"""
LKS HUB Business Intelligence Engine v1

Reads:
    output/scored_articles.json

Creates:
    output/business_intelligence.json

Uses only the Python standard library.
"""

import json
import os
from collections import defaultdict

INPUT_FILE = "output/scored_articles.json"
OUTPUT_FILE = "output/business_intelligence.json"

TOP_ARTICLES_PER_CATEGORY = 5


def load_articles():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_report(articles):

    grouped = defaultdict(list)

    for article in articles:
        category = article.get("category", "Unknown")
        grouped[category].append(article)

    report = {}

    for category, items in grouped.items():

        items.sort(
            key=lambda item: item.get("ai_score", 0),
            reverse=True
        )

        report[category] = items[:TOP_ARTICLES_PER_CATEGORY]

    return report


def save_report(report):

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)


def print_report(report):

    print("\n" + "=" * 60)
    print("LKS HUB BUSINESS INTELLIGENCE")
    print("=" * 60)

    for category in sorted(report.keys()):

        print(f"\n{category.upper()}")
        print("-" * len(category))

        for index, article in enumerate(report[category], start=1):

            print(
                f"{index}. "
                f"[{article['ai_score']:3}] "
                f"{article['title']}"
            )

    print("\n" + "=" * 60)


def main():

    print("LKS HUB Business Intelligence Engine")

    articles = load_articles()

    print(f"Articles loaded : {len(articles)}")

    report = build_report(articles)

    save_report(report)

    print_report(report)

    print(f"\nReport saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()