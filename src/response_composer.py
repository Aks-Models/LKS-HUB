"""
LKS HUB Response Composer v1

Turns retrieved structured knowledge into natural, client-ready answers.

Free-first local version.
"""

from typing import Any


def normalize(text: str) -> str:
    return str(text or "").lower().strip()


def collect_values(
    results: list[dict[str, Any]],
    domain: str | None = None,
    contains_any: set[str] | None = None,
    limit: int = 8
) -> list[str]:
    values = []

    for item in results:
        item_domain = normalize(item.get("domain"))
        item_path = normalize(item.get("item_path"))
        value = str(item.get("value", "")).strip()
        searchable = f"{item_path} {normalize(value)}"

        if domain and item_domain != normalize(domain):
            continue

        if contains_any and not any(
            term in searchable
            for term in contains_any
        ):
            continue

        if value and value not in values:
            values.append(value)

        if len(values) >= limit:
            break

    return values


def compose_lks_vs_aks(
    results: list[dict[str, Any]]
) -> str:
    return """
LKS-HUB and AKS MODELS are related through Luis Kassem Sanz, but they are not the same entity.

LKS-HUB is Luis Kassem Sanz's personal freelancer intelligence, knowledge, automation and AI-assistant platform. Its purpose is to support lks.wh.sk, including the Insights section, the future website assistant, business-intelligence functions and social-media content workflows.

AKS MODELS spol. s r.o. is a separate Slovak legal company founded by Luis. It has its own corporate identity, company website, services and governance.

The intended structure is:

- LKS-HUB = Luis Kassem Sanz's freelancer platform
- lks.wh.sk = Luis's freelancer website
- AKS MODELS = separate company
- AKS-HUB = future separate company platform
- aksmodels.com = AKS MODELS company website

Some technical components developed for LKS-HUB may later be reused, but the knowledge bases, branding, assistants and repositories should remain separate.
""".strip()


def compose_lks_hub_description(
    results: list[dict[str, Any]]
) -> str:
    return """
LKS-HUB is the personal intelligence, knowledge-management, automation and AI-assistant platform created for Luis Kassem Sanz.

Its main purpose is to support lks.wh.sk by providing:

- curated news and Insights
- business-intelligence summaries
- a verified knowledge base about Luis and his services
- an AI assistant for website visitors
- social-media draft generation
- future workflow automation

The current system already includes RSS collection, duplicate detection, relevance scoring, SQLite knowledge storage, intent routing, unified retrieval, local AI-style reasoning, website export and social-media drafting.

It is currently an operational local prototype. Full deployment to lks.wh.sk and production AI integration are still future development steps.
""".strip()


def compose_assistant_capabilities(
    results: list[dict[str, Any]]
) -> str:
    return """
The LKS AI Assistant is designed to answer questions from several verified knowledge domains.

It can currently:

- explain who Luis Kassem Sanz is
- describe his professional, academic and international background
- recommend relevant freelancer services
- explain LKS-HUB and related projects
- distinguish LKS-HUB from AKS MODELS
- search and summarize stored news intelligence
- identify relevant developments by topic
- prepare draft social-media content

The current version works locally using structured JSON files, SQLite and rule-based retrieval. It does not yet use a full production language model and is not yet embedded into lks.wh.sk.
""".strip()


def compose_social_automation_answer(
    results: list[dict[str, Any]]
) -> str:
    return """
LKS-HUB can currently generate draft content for LinkedIn, Facebook and Instagram, but it does not yet publish those posts automatically.

The intended workflow is:

1. LKS-HUB identifies relevant high-value intelligence.
2. The assistant prepares platform-specific drafts.
3. Luis reviews and approves the content.
4. A future publishing integration sends the approved post to the selected platform.

Human approval should remain part of the workflow to prevent inaccurate, unsuitable or unverified content from being published automatically.
""".strip()


def compose_deployment_answer(
    results: list[dict[str, Any]]
) -> str:
    return """
The LKS AI Assistant is not yet deployed on lks.wh.sk.

At present, the intelligence dashboard, knowledge base and assistant operate as a local prototype inside the LKS-HUB project.

The next deployment stages are:

1. create an assistant-facing local or web API
2. connect the website to that API
3. embed the assistant into lks.wh.sk
4. deploy the Insights data feed
5. add privacy, security and rate-limiting controls
6. test the production version before public release
""".strip()


def compose_who_is_luis(
    results: list[dict[str, Any]]
) -> str:
    summaries = collect_values(
        results,
        domain="luis_profile",
        contains_any={
            "short_bio",
            "professional_overview",
            "professional_identity"
        },
        limit=3
    )

    if summaries:
        return "\n\n".join(summaries)

    return (
        "Luis Kassem Sanz is a multilingual Spanish freelancer, entrepreneur "
        "and international business-development professional based in Bratislava. "
        "His background includes diplomatic and consular support, business development, "
        "commercial relations, translation, academic teaching, AI-assisted intelligence "
        "systems and creative work."
    )


def compose_services_answer(
    results: list[dict[str, Any]]
) -> str:
    return """
Luis offers freelance services across several connected areas:

- international business development
- business intelligence and market research
- international expansion and market-entry support
- Saudi Arabia and Middle East business support
- AI-assisted intelligence and automation
- project and meeting coordination
- translation and interpretation
- corporate communications and public relations
- creative and media services

The correct service package depends on the client's market, objectives, required deliverables and timetable. Prices and availability must be confirmed through an initial consultation.
""".strip()


def compose_academic_answer(
    results: list[dict[str, Any]]
) -> str:
    return """
Luis has verified academic teaching experience in Slovakia.

Between 2015 and 2017, he contributed as an Assistant Professor / Teaching Assistant to the courses Colonialism and Orientalism at:

- Matej Bel University in Banská Bystrica
- Comenius University in Bratislava
- Constantine the Philosopher University in Nitra

His responsibilities included course preparation and design, presentation of course material, teaching support, grading-system administration and evaluation of student work.
""".strip()


def compose_saudi_answer(
    results: list[dict[str, Any]]
) -> str:
    return """
Luis has substantial documented professional experience in Riyadh, Saudi Arabia.

His roles included:

- Business Development Manager
- Real Madrid Account Manager
- Sports Services Manager
- Assistant Club Director
- Marketing Communications Executive

This experience involved business development, commercial relations, account management, partner communication, sports services, corporate representation and marketing communications.

Because of that background, Luis can support companies exploring Saudi Arabia with market research, stakeholder identification, Arabic-English business communication, meeting preparation, cross-cultural guidance and commercial follow-up. Legal, tax, licensing and regulated investment matters require appropriately licensed Saudi professionals.
""".strip()


def compose_general_answer(
    question: str,
    results: list[dict[str, Any]]
) -> str:
    relevant_values = collect_values(
        results,
        limit=6
    )

    if not relevant_values:
        return (
            "I could not find enough verified information to answer this question reliably. "
            "The assistant will not invent an answer."
        )

    introduction = (
        "Based on the verified LKS-HUB knowledge base, the following information is relevant:"
    )

    items = "\n".join(
        f"- {value}"
        for value in relevant_values
    )

    return f"{introduction}\n\n{items}"


def compose_response(
    question: str,
    results: list[dict[str, Any]]
) -> str:
    text = normalize(question)

    if (
        "difference" in text
        and "lks" in text
        and "aks" in text
    ):
        return compose_lks_vs_aks(results)

    if (
        "what is lks" in text
        or "what is lks-hub" in text
        or "tell me about lks" in text
    ):
        return compose_lks_hub_description(results)

    if (
        "what can" in text
        and "assistant" in text
    ):
        return compose_assistant_capabilities(results)

    if (
        "automatically publish" in text
        or "automatic publishing" in text
        or "publish posts" in text
        or "social media" in text
    ):
        return compose_social_automation_answer(results)

    if (
        "deployed" in text
        or "already live" in text
        or "on lks.wh.sk" in text
    ):
        return compose_deployment_answer(results)

    if (
        "who is luis" in text
        or "who is luis kassem sanz" in text
    ):
        return compose_who_is_luis(results)

    if (
        "what services" in text
        or "services does luis" in text
        or "what does luis offer" in text
    ):
        return compose_services_answer(results)

    if (
        "academic" in text
        or "university" in text
        or "professor" in text
        or "teaching" in text
    ):
        return compose_academic_answer(results)

    if (
        "saudi" in text
        or "riyadh" in text
    ):
        return compose_saudi_answer(results)

    return compose_general_answer(
        question=question,
        results=results
    )