"""
LKS HUB Knowledge Summary v1
"""

import sqlite3


DATABASE_FILE = "data/lks_knowledge_base.db"


def connect_database():
    return sqlite3.connect(DATABASE_FILE)


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    connection = connect_database()
    cursor = connection.cursor()

    print_section("LKS HUB KNOWLEDGE SUMMARY")

    cursor.execute("SELECT COUNT(*) FROM articles")
    total = cursor.fetchone()[0]
    print(f"Total stored articles: {total}")

    print_section("ARTICLES BY CATEGORY")
    cursor.execute("""
        SELECT category, COUNT(*)
        FROM articles
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)
    for category, count in cursor.fetchall():
        print(f"- {category}: {count}")

    print_section("TOP SCORED ARTICLES")
    cursor.execute("""
        SELECT title, source, category, ai_score, priority_level
        FROM articles
        ORDER BY ai_score DESC
        LIMIT 10
    """)
    for index, row in enumerate(cursor.fetchall(), start=1):
        title, source, category, score, priority = row
        print(f"{index}. [{score}] {title}")
        print(f"   {source} | {category} | {priority}")

    print_section("RECENT HIGH PRIORITY")
    cursor.execute("""
        SELECT title, source, category, published, ai_score
        FROM articles
        WHERE priority_level = 'High'
        ORDER BY id DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No high-priority articles found yet.")
    else:
        for index, row in enumerate(rows, start=1):
            title, source, category, published, score = row
            print(f"{index}. [{score}] {title}")
            print(f"   {source} | {category} | {published}")

    connection.close()


if __name__ == "__main__":
    main()