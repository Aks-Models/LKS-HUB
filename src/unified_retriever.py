"""
LKS HUB Unified Retriever v2

Improved relevance scoring for:
    - News articles
    - Luis profile
    - Services
    - Projects

Removes low-value metadata and prioritizes meaningful matches.
"""

import re
import sqlite3
from typing import Any


DATABASE_FILE = "data/lks_knowledge_base.db"

STOP_WORDS = {
    "a", "an", "and", "are", "about", "can", "could", "do", "does",
    "for", "from", "give", "happening", "in", "is", "latest", "me",
    "my", "news", "of", "on", "or", "please", "show", "summarize",
    "summary", "tell", "the", "to", "today", "what", "who", "with",
    "would", "should"
}

LOW_VALUE_KEYWORDS = {
    "luis",
    "company",
    "business"
}

EXCLUDED_PATHS = {
    "domain",
    "version",
    "updated_at",
    "profile_status"
}

EXCLUDED_PATH_PARTS = {
    "assistant_rules",
    "assistant_guidance",
    "public_information",
    "evidence_register",
    "evidence_basis"
}


def extract_keywords(query: str) -> list[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9]+", query.lower())

    keywords = [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]

    return keywords or [query.lower().strip()]


def connect_database() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def is_useful_path(item_path: str) -> bool:
    normalized_path = item_path.lower().strip()

    if normalized_path in EXCLUDED_PATHS:
        return False

    return not any(
        excluded_part in normalized_path
        for excluded_part in EXCLUDED_PATH_PARTS
    )


def keyword_weight(keyword: str) -> int:
    if keyword in LOW_VALUE_KEYWORDS:
        return 1

    return 5


def score_domain_result(
    result: dict[str, Any],
    keywords: list[str],
    query: str
) -> int:
    domain = str(result.get("domain", "")).lower()
    item_path = str(result.get("item_path", "")).lower()
    value = str(result.get("value", "")).lower()
    query_lower = query.lower()

    score = 0

    for keyword in keywords:
        weight = keyword_weight(keyword)

        if keyword in value:
            score += weight

        if keyword in item_path:
            score += max(1, weight - 1)

        if keyword in domain:
            score += 1

    important_phrases = [
        "saudi arabia",
        "middle east",
        "business development",
        "international expansion",
        "market entry",
        "commercial representation",
        "business intelligence",
        "translation and interpretation",
        "project management",
        "ai and automation"
    ]

    for phrase in important_phrases:
        if phrase in query_lower and phrase in f"{item_path} {value}":
            score += 15

    service_intent_words = {
        "help",
        "expand",
        "expansion",
        "offer",
        "service",
        "services",
        "support",
        "consulting"
    }

    if any(word in query_lower for word in service_intent_words):
        if domain == "services":
            score += 12

    if "saudi arabia" in query_lower:
        if "saudi arabia" in value:
            score += 18

        if domain == "luis_profile" and (
            "saudi arabia" in value
            or "riyadh" in value
        ):
            score += 8

    if "middle east" in query_lower:
        if "middle east" in value:
            score += 15

        if domain == "services":
            score += 6

    return score


def score_news_result(
    result: dict[str, Any],
    keywords: list[str]
) -> int:
    searchable = (
        f"{result.get('title', '')} "
        f"{result.get('source', '')} "
        f"{result.get('category', '')} "
        f"{result.get('region', '')} "
        f"{result.get('country', '')}"
    ).lower()

    keyword_score = 0

    for keyword in keywords:
        if keyword in searchable:
            keyword_score += keyword_weight(keyword) * 2

    ai_score = int(result.get("ai_score", 0) or 0)

    return keyword_score + ai_score


def retrieve_news(
    connection: sqlite3.Connection,
    keywords: list[str],
    limit: int
) -> list[dict[str, Any]]:
    cursor = connection.cursor()

    where_parts = []
    params = []

    for keyword in keywords:
        search_term = f"%{keyword}%"

        where_parts.append("""
            (
                LOWER(title) LIKE ?
                OR LOWER(source) LIKE ?
                OR LOWER(category) LIKE ?
                OR LOWER(region) LIKE ?
                OR LOWER(country) LIKE ?
                OR LOWER(priority_level) LIKE ?
            )
        """)

        params.extend([
            search_term,
            search_term,
            search_term,
            search_term,
            search_term,
            search_term
        ])

    where_clause = " OR ".join(where_parts)

    cursor.execute(f"""
        SELECT
            id,
            title,
            link,
            published,
            source,
            category,
            region,
            country,
            language,
            ai_score,
            priority_level
        FROM articles
        WHERE {where_clause}
        ORDER BY ai_score DESC, id DESC
        LIMIT ?
    """, (*params, limit * 3))

    results = []

    for row in cursor.fetchall():
        item = dict(row)
        item["result_type"] = "news"
        item["domain"] = "news"
        results.append(item)

    return results


def retrieve_domain_knowledge(
    connection: sqlite3.Connection,
    keywords: list[str],
    domains: list[str] | None,
    limit: int
) -> list[dict[str, Any]]:
    cursor = connection.cursor()

    keyword_parts = []
    params = []

    for keyword in keywords:
        keyword_parts.append("LOWER(searchable_text) LIKE ?")
        params.append(f"%{keyword}%")

    where_clause = "(" + " OR ".join(keyword_parts) + ")"

    if domains:
        placeholders = ", ".join("?" for _ in domains)
        where_clause += f" AND domain IN ({placeholders})"
        params.extend(domains)

    cursor.execute(f"""
        SELECT
            id,
            domain,
            item_path,
            value,
            searchable_text
        FROM knowledge_items
        WHERE {where_clause}
        LIMIT ?
    """, (*params, limit * 8))

    results = []

    for row in cursor.fetchall():
        item = dict(row)

        if not is_useful_path(item.get("item_path", "")):
            continue

        item["result_type"] = "domain_knowledge"
        results.append(item)

    return results


def retrieve_all(
    query: str,
    include_news: bool = True,
    domains: list[str] | None = None,
    news_limit: int = 10,
    domain_limit: int = 12
) -> dict[str, Any]:
    keywords = extract_keywords(query)
    connection = connect_database()

    try:
        news_results = []

        if include_news:
            news_results = retrieve_news(
                connection=connection,
                keywords=keywords,
                limit=news_limit
            )

            for result in news_results:
                result["retrieval_score"] = score_news_result(
                    result=result,
                    keywords=keywords
                )

            news_results.sort(
                key=lambda item: item["retrieval_score"],
                reverse=True
            )

            news_results = news_results[:news_limit]

        domain_results = retrieve_domain_knowledge(
            connection=connection,
            keywords=keywords,
            domains=domains,
            limit=domain_limit
        )

        for result in domain_results:
            result["retrieval_score"] = score_domain_result(
                result=result,
                keywords=keywords,
                query=query
            )

        domain_results = [
            result
            for result in domain_results
            if result["retrieval_score"] >= 4
        ]

        domain_results.sort(
            key=lambda item: item["retrieval_score"],
            reverse=True
        )

        domain_results = domain_results[:domain_limit]

        return {
            "query": query,
            "keywords": keywords,
            "news": news_results,
            "domain_knowledge": domain_results
        }

    finally:
        connection.close()


def print_results(results: dict[str, Any]) -> None:
    print("\n" + "=" * 70)
    print("LKS HUB UNIFIED RETRIEVER v2")
    print("=" * 70)
    print(f"Query    : {results['query']}")
    print(f"Keywords : {', '.join(results['keywords'])}")

    print("\nPERSONAL / BUSINESS KNOWLEDGE")
    print("-" * 70)

    domain_results = results["domain_knowledge"]

    if not domain_results:
        print("No matching domain knowledge found.")
    else:
        for index, item in enumerate(domain_results, start=1):
            print(
                f"{index}. [{item['domain']}] "
                f"{item['item_path']} "
                f"[score: {item['retrieval_score']}]"
            )
            print(f"   {item['value']}")

    print("\nNEWS INTELLIGENCE")
    print("-" * 70)

    news_results = results["news"]

    if not news_results:
        print("No matching news found.")
    else:
        for index, item in enumerate(news_results, start=1):
            print(
                f"{index}. [{item['ai_score']}] "
                f"{item['title']}"
            )
            print(
                f"   {item['source']} | "
                f"{item['category']} | "
                f"{item['country']}"
            )
            print(f"   {item['link']}")


def main() -> None:
    print("LKS HUB Unified Retriever v2")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nSearch all LKS knowledge > ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            print("Please enter a question.")
            continue

        results = retrieve_all(query)
        print_results(results)


if __name__ == "__main__":
    main()