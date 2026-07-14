"""
LKS-HUB Culture RSS Feeds
"""

CULTURE_FEEDS = [

    {
        "id": "google_news_culture",
        "name": "Google News Culture",
        "category": "Culture",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 7,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/search?q=culture+arts+film+music+theatre&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "bbc_culture",
        "name": "BBC Culture",
        "category": "Culture",
        "region": "Europe",
        "country": "United Kingdom",
        "language": "en",
        "priority": 8,
        "reliability": 9,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:bbc.com/culture&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "guardian_culture",
        "name": "The Guardian Culture",
        "category": "Culture",
        "region": "Europe",
        "country": "United Kingdom",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "newspaper",
        "active": True,
        "url": "https://www.theguardian.com/uk/culture/rss"
    }

]