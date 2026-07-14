"""
LKS HUB AI v7

Routes current-events questions exclusively to the news database
and uses the Response Composer for personal, service and project questions.
"""

from collections import Counter
from typing import Any

from intent_router import detect_domains
from response_composer import compose_response
from unified_retriever import retrieve_all


PERSONAL_DOMAINS = {
    "luis_profile",
    "services",
    "projects",
}


def build_news_answer(
    question: str,
    news_results: list[dict[str, Any]],
) -> str:
    if not news_results:
        return (
            "I could not find relevant current intelligence for this question "
            "in the LKS-HUB news database."
        )

    categories = Counter(
        article.get("category", "Unknown")
        for article in news_results
    )

    sources = Counter(
        article.get("source", "Unknown")
        for article in news_results
    )

    lines = [
        "CURRENT INTELLIGENCE SUMMARY",
        "-" * 70,
        (
            f"LKS-HUB found {len(news_results)} relevant stored developments "
            f"for: {question}"
        ),
    ]

    if categories:
        lines.append(
            "Main coverage areas: "
            + ", ".join(
                f"{name} ({count})"
                for name, count in categories.most_common(3)
            )
            + "."
        )

    lines.extend([
        "",
        "TOP DEVELOPMENTS",
        "-" * 70,
    ])

    for index, article in enumerate(news_results[:8], start=1):
        title = article.get("title", "Untitled article")
        source = article.get("source", "Unknown source")
        category = article.get("category", "Unknown")
        published = article.get("published", "Date unavailable")
        score = article.get("ai_score", 0)
        link = article.get("link", "")

        lines.append(f"{index}. [{score}] {title}")
        lines.append(f"   Source: {source}")
        lines.append(f"   Category: {category}")
        lines.append(f"   Published: {published}")

        if link:
            lines.append(f"   Link: {link}")

        lines.append("")

    if sources:
        lines.extend([
            "SOURCE COVERAGE",
            "-" * 70,
            ", ".join(
                f"{name} ({count})"
                for name, count in sources.most_common(5)
            ),
        ])

    lines.extend([
        "",
        (
            "This summary reflects articles stored during the latest completed "
            "LKS-HUB pipeline run. It should not be described as real-time unless "
            "the pipeline has just been refreshed."
        ),
    ])

    return "\n".join(lines)


def answer(question: str) -> str:
    routed_domains = detect_domains(question)

    # Current-news questions must not retrieve Luis/profile knowledge.
    if routed_domains == ["news"]:
        results = retrieve_all(
            query=question,
            include_news=True,
            domains=["__news_only__"],
            news_limit=10,
            domain_limit=1,
        )

        composed_answer = build_news_answer(
            question=question,
            news_results=results.get("news", []),
        )

    else:
        personal_domains = [
            domain
            for domain in routed_domains
            if domain in PERSONAL_DOMAINS
        ]

        results = retrieve_all(
            query=question,
            include_news="news" in routed_domains,
            domains=personal_domains or ["__none__"],
            news_limit=6,
            domain_limit=20,
        )

        composed_answer = compose_response(
            question=question,
            results=results.get("domain_knowledge", []),
        )

        if "news" in routed_domains:
            news_section = build_news_answer(
                question=question,
                news_results=results.get("news", []),
            )

            composed_answer = (
                f"{composed_answer}\n\n"
                f"{news_section}"
            )

    response = [
        "",
        "LKS HUB AI RESPONSE",
        "=" * 70,
        f"Question: {question}",
        f"Knowledge route: {', '.join(routed_domains)}",
        "",
        composed_answer,
        "",
        "VERIFICATION NOTE",
        "-" * 70,
        (
            "This answer uses structured LKS-HUB knowledge and stored "
            "intelligence. The assistant does not invent facts or claim "
            "real-time coverage without a current pipeline run."
        ),
    ]

    return "\n".join(response)


def main() -> None:
    print("LKS HUB AI v7")
    print("Intent-Aware Personal Knowledge + News Intelligence")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk LKS AI > ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            print("Please enter a question.")
            continue

        print(answer(question))


if __name__ == "__main__":
    main()