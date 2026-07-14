"""
LKS HUB Assistant v2
Free-first assistant using the local Knowledge Base.
"""

from collections import Counter
from knowledge_retriever import retrieve


def build_summary(question, articles):
    categories = Counter(article.get("category", "Unknown") for article in articles)
    countries = Counter(article.get("country", "Unknown") for article in articles if article.get("country"))

    response = []

    response.append("\nLKS HUB ASSISTANT RESPONSE")
    response.append("=" * 60)
    response.append(f"Question: {question}")

    response.append("\nSummary:")
    response.append("-" * 60)
    response.append(f"I found {len(articles)} relevant intelligence items in the Knowledge Base.")

    if categories:
        top_categories = ", ".join([f"{name} ({count})" for name, count in categories.most_common(3)])
        response.append(f"Main categories: {top_categories}.")

    if countries:
        top_countries = ", ".join([f"{name} ({count})" for name, count in countries.most_common(3)])
        response.append(f"Main countries/locations: {top_countries}.")

    response.append("\nTop relevant items:")
    response.append("-" * 60)

    for index, article in enumerate(articles, start=1):
        response.append(f"{index}. [{article['ai_score']}] {article['title']}")
        response.append(f"   Source   : {article['source']}")
        response.append(f"   Category : {article['category']}")
        response.append(f"   Country  : {article['country']}")
        response.append(f"   Link     : {article['link']}")
        response.append("")

    response.append("Assistant note:")
    response.append("-" * 60)
    response.append(
        "This is a free-first local assistant response. The next version will connect "
        "this retrieved intelligence to an LLM so it can write natural summaries, "
        "strategic analysis, and social media drafts."
    )

    return "\n".join(response)


def answer_question(question):
    articles = retrieve(question, limit=8)

    if not articles:
        return "I found no relevant intelligence in the current Knowledge Base."

    return build_summary(question, articles)


def main():
    print("LKS HUB Assistant v2")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk LKS HUB Assistant > ")

        if question.lower() in ("exit", "quit"):
            break

        print(answer_question(question))


if __name__ == "__main__":
    main()