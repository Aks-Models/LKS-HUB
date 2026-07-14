"""
LKS HUB Full Pipeline Runner
"""

import subprocess
import sys


STEPS = [
    ("RSS Collector", "src/rss/rss_collector.py"),
    ("Duplicate Detector", "src/rss/duplicate_detector.py"),
    ("AI Scorer", "src/rss/ai_scorer.py"),
    ("Knowledge Base", "src/knowledge_base.py"),
    ("Business Intelligence", "src/business_intelligence.py"),
    ("Daily Digest", "src/daily_digest.py"),
    ("Website Export", "src/website_export.py"),
]


def run_step(name, path):
    print("\n" + "=" * 60)
    print(f"RUNNING: {name}")
    print("=" * 60)

    result = subprocess.run([sys.executable, path])

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)

    print(f"\nCOMPLETED: {name}")


def main():
    print("\n" + "=" * 60)
    print("LKS HUB PIPELINE STARTED")
    print("=" * 60)

    for name, path in STEPS:
        run_step(name, path)

    print("\n" + "=" * 60)
    print("LKS HUB PIPELINE COMPLETE")
    print("=" * 60)
    print("Output files updated:")
    print("- output/rss_articles.json")
    print("- output/clean_articles.json")
    print("- output/scored_articles.json")
    print("- data/lks_knowledge_base.db")
    print("- output/business_intelligence.json")
    print("- output/daily_digest.json")
    print("- public/website_data.json")


if __name__ == "__main__":
    main()