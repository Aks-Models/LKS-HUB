"""
LKS HUB Domain Knowledge v1

Loads and searches structured knowledge domains:

    knowledge/luis_profile.json
    knowledge/services.json
    knowledge/projects.json

Python standard library only.
"""

import json
from pathlib import Path
from typing import Any


KNOWLEDGE_DIR = Path("knowledge")

DOMAIN_FILES = {
    "luis_profile": KNOWLEDGE_DIR / "luis_profile.json",
    "services": KNOWLEDGE_DIR / "services.json",
    "projects": KNOWLEDGE_DIR / "projects.json",
}


def load_json_file(file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Knowledge file must contain a JSON object: {file_path}")

    return data


def load_all_domains() -> dict[str, dict[str, Any]]:
    domains = {}

    for domain_name, file_path in DOMAIN_FILES.items():
        domains[domain_name] = load_json_file(file_path)

    return domains


def flatten_json(value: Any, path: str = "") -> list[dict[str, str]]:
    records = []

    if isinstance(value, dict):
        for key, nested_value in value.items():
            next_path = f"{path}.{key}" if path else key
            records.extend(flatten_json(nested_value, next_path))

    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            next_path = f"{path}[{index}]"
            records.extend(flatten_json(nested_value, next_path))

    elif value is not None:
        text = str(value).strip()

        if text:
            records.append({
                "path": path,
                "value": text
            })

    return records


def search_domain(
    query: str,
    domain_name: str,
    limit: int = 10
) -> list[dict[str, str]]:
    if domain_name not in DOMAIN_FILES:
        raise ValueError(f"Unknown knowledge domain: {domain_name}")

    domain_data = load_json_file(DOMAIN_FILES[domain_name])
    records = flatten_json(domain_data)

    query_words = [
        word.lower()
        for word in query.split()
        if len(word.strip()) > 1
    ]

    matches = []

    for record in records:
        searchable_text = (
            f"{record['path']} {record['value']}"
        ).lower()

        score = sum(
            1 for word in query_words
            if word in searchable_text
        )

        if score > 0:
            matches.append({
                "domain": domain_name,
                "path": record["path"],
                "value": record["value"],
                "match_score": score
            })

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return matches[:limit]


def search_all_domains(
    query: str,
    limit_per_domain: int = 5
) -> dict[str, list[dict[str, str]]]:
    results = {}

    for domain_name in DOMAIN_FILES:
        domain_results = search_domain(
            query=query,
            domain_name=domain_name,
            limit=limit_per_domain
        )

        if domain_results:
            results[domain_name] = domain_results

    return results


def print_results(
    query: str,
    results: dict[str, list[dict[str, str]]]
) -> None:
    print("\n" + "=" * 70)
    print(f"LKS HUB DOMAIN KNOWLEDGE SEARCH: {query}")
    print("=" * 70)

    if not results:
        print("No matching personal knowledge found.")
        return

    for domain_name, domain_results in results.items():
        print(f"\nDOMAIN: {domain_name.upper()}")
        print("-" * 70)

        for index, result in enumerate(domain_results, start=1):
            print(
                f"{index}. {result['path']} "
                f"[score: {result['match_score']}]"
            )
            print(f"   {result['value']}")


def main() -> None:
    print("LKS HUB Domain Knowledge v1")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nSearch personal knowledge > ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            print("Please enter a search term.")
            continue

        results = search_all_domains(query)
        print_results(query, results)


if __name__ == "__main__":
    main()