"""
LKS HUB Knowledge Retriever v2
Natural-language keyword retrieval from the Knowledge Base.
"""

import re
import sqlite3


DATABASE_FILE = "data/lks_knowledge_base.db"

STOP_WORDS = {
    "what", "is", "are", "the", "in", "on", "at", "to", "from", "about",
    "happening", "summarize", "summary", "news", "today", "latest",
    "please", "show", "me", "tell", "give", "and", "or", "of", "for",
    "with", "a", "an"
}


def extract_keywords(query):
    words = re.findall(r"[A-Za-z0-9]+", query.lower())

    keywords = [
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]

    return keywords or [query.lower()]


def retrieve(query, limit=10):
    keywords = extract_keywords(query)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    where_parts = []
    params = []

    for keyword in keywords:
        search = f"%{keyword}%"

        where_parts.append("""
        (
            LOWER(title) LIKE ?
            OR LOWER(category) LIKE ?
            OR LOWER(source) LIKE ?
            OR LOWER(country) LIKE ?
            OR LOWER(region) LIKE ?
            OR LOWER(priority_level) LIKE ?
        )
        """)

        params.extend([search, search, search, search, search, search])

    where_clause = " OR ".join(where_parts)

    params.append(limit)

    cursor.execute(f"""
        SELECT *
        FROM articles
        WHERE {where_clause}
        ORDER BY ai_score DESC
        LIMIT ?
    """, params)

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    while True:
        question = input("\nAsk LKS HUB > ")

        if question.lower() in ("exit", "quit"):
            break

        articles = retrieve(question)

        print(f"\nFound {len(articles)} relevant articles:\n")

        for i, article in enumerate(articles, start=1):
            print(f"{i}. [{article['ai_score']}] {article['title']}")
            print(f"   Source   : {article['source']}")
            print(f"   Category : {article['category']}")
            print(f"   Country  : {article['country']}")
            print()