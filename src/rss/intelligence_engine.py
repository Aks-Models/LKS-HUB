"""
LKS HUB Intelligence Engine

Purpose:
Evaluate RSS articles and determine whether they are relevant
to the LKS HUB Knowledge Base.
"""

KEYWORDS = {
    "artificial intelligence": 100,
    "ai": 100,
    "automation": 90,
    "business": 90,
    "freelance": 90,
    "marketing": 80,
    "web development": 80,
    "python": 80,
    "github": 75,
    "slovakia": 90,
    "european union": 85,
    "casting": 75,
    "acting": 75,
}


MINIMUM_SCORE = 70


def score_article(title):
    score = 0
    title = title.lower()

    for keyword, value in KEYWORDS.items():
        if keyword in title:
            score += value

    return score


def is_relevant(title):
    return score_article(title) >= MINIMUM_SCORE


def main():
    sample_titles = [
        "New AI tools for freelancers",
        "Football transfer rumours",
        "Slovakia introduces new tax rules",
        "Casting opportunity in Prague",
    ]

    print("LKS HUB Intelligence Engine\n")

    for title in sample_titles:
        score = score_article(title)

        if is_relevant(title):
            status = "KEEP"
        else:
            status = "IGNORE"

        print(f"{status:7} | {score:3} | {title}")


if __name__ == "__main__":
    main()
