"""
LKS HUB Social Post Generator v1
Creates draft LinkedIn/Facebook/Instagram posts from Knowledge Base intelligence.
"""

from knowledge_retriever import retrieve


def create_linkedin_post(topic, articles):
    if not articles:
        return "No relevant articles found for this topic."

    top = articles[0]

    return f"""
LINKEDIN POST DRAFT
==============================

{topic.title()} is becoming an important topic to watch.

One relevant development:
"{top.get("title", "")}"

Why it matters:
This may have implications for business, technology, security, markets, or regional strategy depending on how the situation develops.

Source:
{top.get("source", "")}

Read more:
{top.get("link", "")}

#BusinessIntelligence #AI #GlobalNews #LKSHUB
"""


def create_facebook_post(topic, articles):
    if not articles:
        return "No relevant articles found for this topic."

    top = articles[0]

    return f"""
FACEBOOK POST DRAFT
==============================

Interesting update about {topic}:

{top.get("title", "")}

Source: {top.get("source", "")}

{top.get("link", "")}
"""


def create_instagram_caption(topic, articles):
    if not articles:
        return "No relevant articles found for this topic."

    top = articles[0]

    return f"""
INSTAGRAM CAPTION DRAFT
==============================

Global intelligence update: {topic}

{top.get("title", "")}

Source: {top.get("source", "")}

#LKSHUB #Intelligence #GlobalNews #Business #AI
"""


def main():
    print("LKS HUB Social Post Generator v1")
    print("Type 'exit' to quit.")

    while True:
        topic = input("\nTopic for social post > ")

        if topic.lower() in ("exit", "quit"):
            break

        articles = retrieve(topic, limit=5)

        print(create_linkedin_post(topic, articles))
        print(create_facebook_post(topic, articles))
        print(create_instagram_caption(topic, articles))


if __name__ == "__main__":
    main()