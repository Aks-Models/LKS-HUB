"""
LKS HUB AI Reasoner v1
Free-first reasoning layer.

Takes retrieved articles and turns them into a structured intelligence briefing.
No external API yet.
"""

from collections import Counter


def assess_risk(articles):
    high_count = sum(1 for article in articles if article.get("priority_level") == "High")
    top_score = max([article.get("ai_score", 0) for article in articles], default=0)

    if high_count >= 3 or top_score >= 90:
        return "High"
    if high_count >= 1 or top_score >= 70:
        return "Medium"
    return "Low"


def reason(question, articles):
    if not articles:
        return "No relevant intelligence found in the Knowledge Base."

    categories = Counter(article.get("category", "Unknown") for article in articles)
    countries = Counter(article.get("country", "Unknown") for article in articles if article.get("country"))
    sources = Counter(article.get("source", "Unknown") for article in articles)

    risk_level = assess_risk(articles)

    briefing = []

    briefing.append("\nLKS HUB INTELLIGENCE BRIEFING")
    briefing.append("=" * 70)
    briefing.append(f"Question: {question}")

    briefing.append("\nExecutive Summary")
    briefing.append("-" * 70)
    briefing.append(
        f"The Knowledge Base found {len(articles)} relevant intelligence items. "
        f"The strongest signals are concentrated in "
        f"{', '.join([name for name, _ in categories.most_common(3)])}. "
        f"Current assessed relevance/risk level: {risk_level}."
    )

    if countries:
        briefing.append(
            f"Main geographic focus: "
            f"{', '.join([name for name, _ in countries.most_common(4)])}."
        )

    briefing.append("\nKey Developments")
    briefing.append("-" * 70)

    for index, article in enumerate(articles[:5], start=1):
        briefing.append(
            f"{index}. [{article.get('ai_score', 0)}] {article.get('title', '')}"
        )
        briefing.append(
            f"   {article.get('source', '')} | {article.get('category', '')} | "
            f"{article.get('country', '')}"
        )

    briefing.append("\nBusiness / Strategic Relevance")
    briefing.append("-" * 70)

    if risk_level == "High":
        briefing.append(
            "This topic should be monitored closely. It may indicate important strategic, "
            "market, security, political, or reputational implications."
        )
    elif risk_level == "Medium":
        briefing.append(
            "This topic has moderate strategic relevance. It is worth tracking, especially "
            "if related stories continue to appear in future pipeline runs."
        )
    else:
        briefing.append(
            "This topic currently appears to have limited strategic urgency, but remains "
            "available in the Knowledge Base for later comparison."
        )

    briefing.append("\nSource Pattern")
    briefing.append("-" * 70)
    briefing.append(
        "Most frequent sources: "
        + ", ".join([f"{name} ({count})" for name, count in sources.most_common(5)])
    )

    briefing.append("\nSuggested Next Actions")
    briefing.append("-" * 70)
    briefing.append("1. Continue monitoring this topic in the next pipeline run.")
    briefing.append("2. If relevance increases, prepare a short social media insight.")
    briefing.append("3. If it relates to LKS services, consider turning it into a LinkedIn post.")

    briefing.append("\nSources")
    briefing.append("-" * 70)

    for article in articles[:8]:
        briefing.append(f"- {article.get('title', '')}")
        briefing.append(f"  {article.get('link', '')}")

    return "\n".join(briefing)