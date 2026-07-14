"""
LKS HUB Duplicate Detector
Reads output/rss_articles.json and creates output/clean_articles.json.
"""

import json
import os
import re

INPUT_FILE = "output/rss_articles.json"
OUTPUT_FILE = "output/clean_articles.json"


def normalize_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def make_duplicate_key(article):
    return normalize_title(article.get("title", ""))


def load_articles():
    if not os.path.exists(INPUT_FILE):
        print(f"Missing input file: {INPUT_FILE}")
        return []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_articles(articles):
    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=2)


def remove_duplicates(articles):
    seen = {}
    clean_articles = []

    for article in articles:

        key = make_duplicate_key(article)

        if key not in seen:
            seen[key] = article
            clean_articles.append(article)

    return clean_articles


def main():

    print("LKS HUB Duplicate Detector")

    articles = load_articles()

    print(f"Original articles : {len(articles)}")

    clean_articles = remove_duplicates(articles)

    print(f"Unique articles   : {len(clean_articles)}")
    print(f"Duplicates removed: {len(articles) - len(clean_articles)}")

    save_articles(clean_articles)

    print(f"Output saved      : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()