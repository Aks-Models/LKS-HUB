"""
LKS HUB Intent Router v2

Classifies questions before retrieval so current-news questions
do not search Luis's personal profile.
"""

import re


CURRENT_NEWS_PHRASES = {
    "what is happening",
    "what's happening",
    "what is going on",
    "what's going on",
    "latest news",
    "current news",
    "latest developments",
    "current developments",
    "news about",
    "updates about",
    "update on",
    "today in",
    "this week in",
    "recent developments",
    "summarize the news",
    "summarize news",
}


NEWS_TOPICS = {
    "ai",
    "artificial intelligence",
    "business",
    "casting",
    "culture",
    "economy",
    "fashion",
    "finance",
    "iran",
    "israel",
    "middle east",
    "politics",
    "saudi arabia",
    "science",
    "security",
    "slovakia",
    "space",
    "technology",
    "ukraine",
    "world",
}


LUIS_KEYWORDS = {
    "luis",
    "luis kassem sanz",
    "kassem",
    "sanz",
    "biography",
    "background",
    "career",
    "education",
    "languages",
    "academic",
    "professor",
    "teaching",
    "experience",
}


SERVICE_KEYWORDS = {
    "service",
    "services",
    "offer",
    "offers",
    "provide",
    "provides",
    "consulting",
    "help my company",
    "business development",
    "market entry",
    "international expansion",
    "translation",
    "interpretation",
    "automation",
    "project management",
}


PROJECT_KEYWORDS = {
    "lks hub",
    "lks-hub",
    "aks models",
    "aksmodels",
    "aks hub",
    "aks-hub",
    "project",
    "projects",
    "platform",
    "assistant",
    "website",
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9À-ÿ\s'-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, phrases: set[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def is_current_news_question(text: str) -> bool:
    if contains_any(text, CURRENT_NEWS_PHRASES):
        return True

    news_time_words = {
        "latest",
        "current",
        "today",
        "recent",
        "now",
        "this week",
        "this month",
    }

    news_activity_words = {
        "news",
        "happening",
        "developments",
        "updates",
        "situation",
        "going on",
    }

    has_time_signal = contains_any(text, news_time_words)
    has_news_signal = contains_any(text, news_activity_words)
    has_topic = contains_any(text, NEWS_TOPICS)

    return has_topic and (has_time_signal or has_news_signal)


def detect_domains(question: str) -> list[str]:
    text = normalize_text(question)

    # Current-events questions must use the news database only.
    if is_current_news_question(text):
        return ["news"]

    domains = []

    if contains_any(text, LUIS_KEYWORDS):
        domains.append("luis_profile")

    if contains_any(text, SERVICE_KEYWORDS):
        domains.append("services")

    if contains_any(text, PROJECT_KEYWORDS):
        domains.append("projects")

    # A question may explicitly combine Luis/services with current news.
    if (
        contains_any(text, NEWS_TOPICS)
        and contains_any(text, {"news", "latest", "current", "developments"})
    ):
        domains.append("news")

    if not domains:
        domains.append("news")

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(domains))


def main() -> None:
    print("LKS HUB Intent Router v2")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a question > ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            print("Please enter a question.")
            continue

        domains = detect_domains(question)

        print("\n" + "=" * 70)
        print("LKS HUB INTENT ROUTER")
        print("=" * 70)
        print(f"Question : {question}")
        print(f"Domains  : {', '.join(domains)}")


if __name__ == "__main__":
    main()