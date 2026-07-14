"""
LKS HUB Domain Indexer v1

Reads structured knowledge files:

    knowledge/luis_profile.json
    knowledge/services.json
    knowledge/projects.json

Creates or updates the `knowledge_items` table inside:

    data/lks_knowledge_base.db

Python standard library only.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any


DATABASE_FILE = "data/lks_knowledge_base.db"

DOMAIN_FILES = {
    "luis_profile": Path("knowledge/luis_profile.json"),
    "services": Path("knowledge/services.json"),
    "projects": Path("knowledge/projects.json"),
}


def load_json(file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in: {file_path}")

    return data


def flatten_json(
    value: Any,
    path: str = ""
) -> list[tuple[str, str]]:
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
            records.append((path, text))

    return records


def connect_database() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_FILE)


def create_table(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            item_path TEXT NOT NULL,
            value TEXT NOT NULL,
            searchable_text TEXT NOT NULL,
            UNIQUE(domain, item_path, value)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_domain
        ON knowledge_items(domain)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_searchable
        ON knowledge_items(searchable_text)
    """)

    connection.commit()


def clear_domain(
    connection: sqlite3.Connection,
    domain_name: str
) -> None:
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM knowledge_items WHERE domain = ?",
        (domain_name,)
    )

    connection.commit()


def insert_domain(
    connection: sqlite3.Connection,
    domain_name: str,
    records: list[tuple[str, str]]
) -> int:
    cursor = connection.cursor()
    inserted = 0

    for item_path, value in records:
        searchable_text = (
            f"{domain_name} {item_path} {value}"
        ).lower()

        cursor.execute("""
            INSERT OR IGNORE INTO knowledge_items (
                domain,
                item_path,
                value,
                searchable_text
            )
            VALUES (?, ?, ?, ?)
        """, (
            domain_name,
            item_path,
            value,
            searchable_text
        ))

        if cursor.rowcount > 0:
            inserted += 1

    connection.commit()

    return inserted


def index_all_domains(
    connection: sqlite3.Connection
) -> dict[str, int]:
    results = {}

    for domain_name, file_path in DOMAIN_FILES.items():
        data = load_json(file_path)
        records = flatten_json(data)

        clear_domain(connection, domain_name)

        inserted = insert_domain(
            connection=connection,
            domain_name=domain_name,
            records=records
        )

        results[domain_name] = inserted

    return results


def print_summary(
    connection: sqlite3.Connection,
    results: dict[str, int]
) -> None:
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM knowledge_items")
    total_items = cursor.fetchone()[0]

    print("\n" + "=" * 70)
    print("LKS HUB DOMAIN INDEX SUMMARY")
    print("=" * 70)

    for domain_name, inserted in results.items():
        print(f"{domain_name:<20}: {inserted}")

    print("-" * 70)
    print(f"Total indexed items : {total_items}")
    print(f"Database            : {DATABASE_FILE}")
    print("=" * 70)


def main() -> None:
    print("LKS HUB Domain Indexer v1")

    connection = connect_database()

    try:
        create_table(connection)

        results = index_all_domains(connection)

        print_summary(
            connection=connection,
            results=results
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()