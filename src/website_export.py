"""
LKS HUB Website Export

Creates a compact JSON file optimized for the website frontend.
"""

import json
import os
from datetime import datetime, timezone


INPUT_FILE = "output/scored_articles.json"
OUTPUT_FILE = "public/website_data.json"
ARTICLES_PER_CATEGORY = 10


def load_articles():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def group_by_category(articles):
    categories = {}

    for article in articles:
        category = article.get("category", "Other")

        if category not in categories:
            categories[category] = []

        categories[category].append(article)

    return categories


def build_export(categories):
    website = {
        "generated_from": "LKS HUB",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "categories": {}
    }

    for category, articles in categories.items():
        website["categories"][category] = []

        for article in articles[:ARTICLES_PER_CATEGORY]:
            website["categories"][category].append({
                "title": article.get("title", ""),
                "link": article.get("link", ""),
                "published": article.get("published", ""),
                "source": article.get("source", ""),
                "category": article.get("category", category),
                "region": article.get("region", ""),
                "country": article.get("country", ""),
                "language": article.get("language", ""),
                "score": article.get("ai_score", 0),
                "priority_level": article.get("priority_level", "Low")
            })

    return website


def save_export(data):
    os.makedirs("public", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def main():
    print("LKS HUB Website Export")

    articles = load_articles()

    print(f"Articles loaded : {len(articles)}")

    categories = group_by_category(articles)

    export = build_export(categories)

    save_export(export)

    print(f"Website JSON saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()