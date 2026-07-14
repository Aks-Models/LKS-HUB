"""
LKS HUB Daily Digest v1

Reads:
    output/business_intelligence.json

Creates:
    output/daily_digest.json

Uses only the Python standard library.
"""

import json
import os
from datetime import datetime, timezone


INPUT_FILE = "output/business_intelligence.json"
OUTPUT_FILE = "output/daily_digest.json"

CATEGORIES_ORDER = [
    "Business",
    "Technology",
    "Security",
    "Science",
    "AI",
    "Finance",
    "Politics",
    "World",
    "Middle East",
    "Slovakia",
    "Space",
    "Fashion",
    "Casting",
    "Culture",
]


def load_business_intelligence():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_digest(report):
    digest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "LKS HUB Daily Intelligence Digest",
        "sections": [],
    }

    for category in CATEGORIES_ORDER:
        articles = report.get(category, [])

        if not articles:
            continue

        section = {
            "category": category,
            "headline": f"Top {category} developments",
            "articles": [],
        }

        for article in articles[:5]:
            section["articles"].append({
                "title": article.get("title", ""),
                "source": article.get("source", ""),
                "published": article.get("published", ""),
                "link": article.get("link", ""),
                "ai_score": article.get("ai_score", 0),
                "priority_level": article.get("priority_level", "Low"),
            })

        digest["sections"].append(section)

    return digest


def save_digest(digest):
    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(digest, file, ensure_ascii=False, indent=2)


def print_digest(digest):
    print("\n" + "=" * 60)
    print(digest["title"])
    print("=" * 60)

    for section in digest["sections"]:
        print(f"\n{section['category'].upper()}")
        print("-" * len(section["category"]))

        for index, article in enumerate(section["articles"], start=1):
            print(f"{index}. [{article['ai_score']:3}] {article['title']}")

    print("\n" + "=" * 60)


def main():
    print("LKS HUB Daily Digest Generator")

    report = load_business_intelligence()

    digest = build_digest(report)

    save_digest(digest)

    print_digest(digest)

    print(f"\nDigest saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()