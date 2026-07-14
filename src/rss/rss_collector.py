"""
LKS HUB RSS Collector
Free-first version using only Python standard library.
"""

import json
import os
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

from feeds import RSS_FEEDS


def fetch_rss(feed_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    request = Request(feed_url, headers=headers)

    with urlopen(request, timeout=20) as response:
        return response.read()


def parse_rss(xml_data):
    root = ET.fromstring(xml_data)
    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else []

    articles = []

    for item in items[:10]:
        articles.append({
            "title": item.findtext("title", default="No title"),
            "link": item.findtext("link", default="No link"),
            "published": item.findtext("pubDate", default="No date"),
        })

    return articles


def main():
    print("LKS HUB RSS Collector started.")

    successful_feeds = 0
    failed_feeds = 0
    total_articles = 0
    all_articles = []

    for feed in RSS_FEEDS:

        if feed.get("active") is False:
            print(f"\nSkipping inactive feed: {feed['name']}")
            continue

        print(f"\nFetching: {feed['name']}")

        try:
            xml_data = fetch_rss(feed["url"])
            articles = parse_rss(xml_data)

            for article in articles:
                article["source"] = feed["name"]
                article["category"] = feed["category"]
                article["region"] = feed.get("region", "")
                article["country"] = feed.get("country", "")
                article["language"] = feed.get("language", "")
                article["retrieved_at"] = datetime.now(timezone.utc).isoformat()

                all_articles.append(article)

            successful_feeds += 1
            total_articles += len(articles)

            print("\nLatest articles:\n")

            for index, article in enumerate(articles, start=1):
                print(f"{index}. {article['title']}")
                print(f"   Date: {article['published']}")
                print(f"   Link: {article['link']}\n")

        except Exception as e:
            failed_feeds += 1
            print(f"FAILED: {e}")

    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    with open("data/rss_articles.json", "w", encoding="utf-8") as file:
        json.dump(all_articles, file, ensure_ascii=False, indent=2)

    with open("output/rss_articles.json", "w", encoding="utf-8") as file:
        json.dump(all_articles, file, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print("LKS HUB RSS SUMMARY")
    print("=" * 50)
    print(f"Successful feeds : {successful_feeds}")
    print(f"Failed feeds     : {failed_feeds}")
    print(f"Articles fetched : {total_articles}")
    print("Data JSON        : data/rss_articles.json")
    print("Output JSON      : output/rss_articles.json")
    print("=" * 50)


if __name__ == "__main__":
    main()