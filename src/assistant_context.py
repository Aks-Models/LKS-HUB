"""
LKS HUB Assistant Context v1
Creates a compact context file for the future AI assistant.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone


DATABASE_FILE = "data/lks_knowledge_base.db"
OUTPUT_FILE = "output/assistant_context.json"


def main():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")
    total_articles = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM articles
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)
    categories = dict(cursor.fetchall())

    cursor.execute("""
        SELECT title, source, category, country, region, ai_score, priority_level, link
        FROM articles
        ORDER BY ai_score DESC
        LIMIT 50
    """)
    top_articles = []

    for row in cursor.fetchall():
        title, source, category, country, region, score, priority, link = row
        top_articles.append({
            "title": title,
            "source": source,
            "category": category,
            "country": country,
            "region": region,
            "ai_score": score,
            "priority_level": priority,
            "link": link
        })

    connection.close()

    context = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "LKS HUB",
        "purpose": "AI assistant context for Luis Kassem Sanz freelancer website and intelligence dashboard.",
        "total_articles": total_articles,
        "categories": categories,
        "top_articles": top_articles
    }

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(context, file, ensure_ascii=False, indent=2)

    print("Assistant context created.")
    print(f"Output saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()