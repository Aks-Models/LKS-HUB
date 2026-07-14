"""
LKS HUB AI Relevance Scorer
Reads output/clean_articles.json and creates output/scored_articles.json.
Free-first rule-based version.
"""

import json
import os
import re


INPUT_FILE = "output/clean_articles.json"
OUTPUT_FILE = "output/scored_articles.json"


CATEGORY_SCORES = {
    "Business": 40,
    "Technology": 40,
    "Finance": 40,
    "Security": 40,
    "Science": 40,

    "AI": 35,
    "Politics": 35,

    "World": 25,
    "Middle East": 25,
    "Slovakia": 25,
    "Space": 25,

    "Fashion": 10,
    "Casting": 10,
    "Culture": 10,
}


SOURCE_BONUSES = {
    "Reuters": 15,
    "BBC": 15,
    "Associated Press": 15,
    "NASA": 15,
    "European Space Agency": 15,
    "CNBC": 12,
    "MarketWatch": 12,
    "Yahoo Finance": 10,
    "TechCrunch": 10,
    "The Verge": 10,
    "Ars Technica": 10,
    "The Hacker News": 10,
    "BleepingComputer": 10,
    "Krebs": 10,
}


KEYWORD_BONUSES = {
    "business": 20,
    "economy": 20,
    "markets": 20,
    "technology": 20,
    "science": 20,
    "security": 20,
    "cyber": 20,

    "artificial intelligence": 20,
    "openai": 20,
    "ai": 15,
    "machine learning": 15,
    "nvidia": 15,
    "microsoft": 15,
    "google": 15,

    "hack": 20,
    "breach": 20,
    "malware": 20,

    "inflation": 15,
    "interest rates": 15,
    "gdp": 15,
    "bitcoin": 15,
    "crypto": 15,

    "war": 15,
    "conflict": 15,
    "election": 15,
    "government": 15,
    "regulation": 15,

    "space": 15,
    "nasa": 15,
    "spacex": 15,

    "luxury": 10,
    "fashion": 10,
    "casting": 10,
    "film": 8,
}


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


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_score(article):
    score = 0

    category = article.get("category", "")
    source = article.get("source", "")
    title = article.get("title", "")

    score += CATEGORY_SCORES.get(category, 5)

    for source_name, bonus in SOURCE_BONUSES.items():
        if source_name.lower() in source.lower():
            score += bonus

    normalized_title = normalize_text(title)

    for keyword, bonus in KEYWORD_BONUSES.items():
        if keyword in normalized_title:
            score += bonus

    return min(score, 100)


def assign_priority(score):
    if score >= 80:
        return "High"
    if score >= 50:
        return "Medium"
    return "Low"


def score_articles(articles):
    scored_articles = []

    for article in articles:
        score = calculate_score(article)

        article["ai_score"] = score
        article["priority_level"] = assign_priority(score)

        scored_articles.append(article)

    scored_articles.sort(key=lambda item: item["ai_score"], reverse=True)

    return scored_articles


def main():
    print("LKS HUB AI Relevance Scorer")

    articles = load_articles()

    print(f"Input articles  : {len(articles)}")

    scored_articles = score_articles(articles)

    print(f"Scored articles : {len(scored_articles)}")

    save_articles(scored_articles)

    print(f"Output saved    : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()