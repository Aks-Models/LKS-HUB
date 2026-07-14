"""
LKS HUB Knowledge Search v1

Searches:
    data/lks_knowledge_base.db

Usage:
    py .\src\knowledge_search.py Iran
    py .\src\knowledge_search.py "Middle East"
"""

import sqlite3
import sys


DATABASE_FILE = "data/lks_knowledge_base.db"


def search_articles(query, limit=10):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    search_term = f"%{query}%"

    cursor.execute("""
        SELECT
            title,
            source,
            category,
            region,
            country,
            published,
            ai_score,
            priority_level,
            link
        FROM articles
        WHERE
            title LIKE ?
            OR source LIKE ?
            OR category LIKE ?
            OR region LIKE ?
            OR country LIKE ?
            OR published LIKE ?
            OR priority_level LIKE ?
        ORDER BY ai_score DESC
        LIMIT ?
    """, (
        search_term,
        search_term,
        search_term,
        search_term,
        search_term,
        search_term,
        search_term,
        limit
    ))

    results = cursor.fetchall()
    connection.close()

    return results


def print_results(query, results):
    print("\n" + "=" * 60)
    print(f"LKS HUB KNOWLEDGE SEARCH: {query}")
    print("=" * 60)

    if not results:
        print("No results found.")
        print("=" * 60)
        return

    for index, article in enumerate(results, start=1):
        title, source, category, region, country, published, ai_score, priority_level, link = article

        print(f"\n{index}. [{ai_score}] {title}")
        print(f"   Source   : {source}")
        print(f"   Category : {category}")
        print(f"   Region   : {region}")
        print(f"   Country  : {country}")
        print(f"   Priority : {priority_level}")
        print(f"   Date     : {published}")
        print(f"   Link     : {link}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print('  py .\\src\\knowledge_search.py Iran')
        print('  py .\\src\\knowledge_search.py "Middle East"')
        return

    query = " ".join(sys.argv[1:])
    results = search_articles(query)

    print_results(query, results)


if __name__ == "__main__":
    main()