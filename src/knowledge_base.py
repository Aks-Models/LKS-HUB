"""
LKS HUB Knowledge Base v1

Reads:
    output/scored_articles.json

Creates / updates:
    data/lks_knowledge_base.db

Uses SQLite and Python standard library only.
"""

import json
import os
import sqlite3


INPUT_FILE = "output/scored_articles.json"
DATABASE_FILE = "data/lks_knowledge_base.db"


def load_articles():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def connect_database():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            published TEXT,
            source TEXT,
            category TEXT,
            region TEXT,
            country TEXT,
            language TEXT,
            ai_score INTEGER,
            priority_level TEXT
        )
    """)

    connection.commit()


def insert_articles(connection, articles):
    cursor = connection.cursor()

    inserted = 0
    skipped = 0

    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO articles (
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
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.get("title", ""),
                article.get("link", ""),
                article.get("published", ""),
                article.get("source", ""),
                article.get("category", ""),
                article.get("region", ""),
                article.get("country", ""),
                article.get("language", ""),
                article.get("ai_score", 0),
                article.get("priority_level", "")
            ))

            inserted += 1

        except sqlite3.IntegrityError:
            skipped += 1

    connection.commit()

    return inserted, skipped


def print_summary(connection, inserted, skipped):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")
    total_articles = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM articles GROUP BY category ORDER BY COUNT(*) DESC")
    category_counts = cursor.fetchall()

    print("\n" + "=" * 60)
    print("LKS HUB KNOWLEDGE BASE SUMMARY")
    print("=" * 60)
    print(f"Inserted this run : {inserted}")
    print(f"Skipped duplicate : {skipped}")
    print(f"Total stored      : {total_articles}")

    print("\nArticles by category:")
    for category, count in category_counts:
        print(f"- {category}: {count}")

    print("=" * 60)


def main():
    print("LKS HUB Knowledge Base Builder")

    articles = load_articles()

    print(f"Articles loaded : {len(articles)}")

    connection = connect_database()

    create_tables(connection)

    inserted, skipped = insert_articles(connection, articles)

    print_summary(connection, inserted, skipped)

    connection.close()

    print(f"\nDatabase saved : {DATABASE_FILE}")


if __name__ == "__main__":
    main()