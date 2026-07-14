"""
LKS HUB Social Export v1
Automatically creates social media draft posts from top scored articles.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone


DATABASE_FILE = "data/lks_knowledge_base.db"
OUTPUT_FILE = "output/social_posts.json"


def load_top_articles(limit=10):
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        ORDER BY ai_score DESC
        LIMIT ?
    """, (limit,))

    articles = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return articles


def create_posts(article):
    title = article.get("title", "")
    source = article.get("source", "")
    category = article.get("category", "")
    link = article.get("link", "")

    return {
        "topic": category,
        "source_article": title,
        "linkedin": (
            f"{category} is an important topic to watch.\n\n"
            f"One current development:\n{title}\n\n"
            f"Why it matters:\nThis may have strategic, business, technological, security, "
            f"or market implications depending on how the situation develops.\n\n"
            f"Source: {source}\n{link}\n\n"
            f"#BusinessIntelligence #LKSHUB #GlobalNews #{category.replace(' ', '')}"
        ),
        "facebook": (
            f"Interesting {category} update:\n\n"
            f"{title}\n\n"
            f"Source: {source}\n{link}"
        ),
        "instagram": (
            f"Global intelligence update: {category}\n\n"
            f"{title}\n\n"
            f"Source: {source}\n\n"
            f"#LKSHUB #Intelligence #GlobalNews #{category.replace(' ', '')}"
        )
    }


def main():
    print("LKS HUB Social Export v1")

    articles = load_top_articles(limit=10)

    posts = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "platforms": ["LinkedIn", "Facebook", "Instagram"],
        "posts": [create_posts(article) for article in articles]
    }

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=2)

    print(f"Social drafts created : {len(posts['posts'])}")
    print(f"Output saved          : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()