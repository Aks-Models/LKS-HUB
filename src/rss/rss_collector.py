"""
LKS HUB RSS Collector
Free-first version using only Python standard library.
"""

import xml.etree.ElementTree as ET
from urllib.request import urlopen


RSS_FEED_URL = "https://news.ycombinator.com/rss"


def fetch_rss(feed_url):
    with urlopen(feed_url, timeout=20) as response:
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

    xml_data = fetch_rss(RSS_FEED_URL)
    articles = parse_rss(xml_data)

    print("\nLatest articles:\n")

    for index, article in enumerate(articles, start=1):
        print(f"{index}. {article['title']}")
        print(f"   Date: {article['published']}")
        print(f"   Link: {article['link']}\n")


if __name__ == "__main__":
    main()
