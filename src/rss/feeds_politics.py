"""
LKS-HUB Politics RSS Feeds
"""

POLITICS_FEEDS = [

    {
        "id": "google_news_politics",
        "name": "Google News Politics",
        "category": "Politics",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 9,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/headlines/section/topic/POLITICS?hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "politico",
        "name": "Politico",
        "category": "Politics",
        "region": "North America",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "political_media",
        "active": True,
        "url": "https://rss.politico.com/politics-news.xml"
    },

    {
        "id": "bbc_politics",
        "name": "BBC Politics",
        "category": "Politics",
        "region": "Europe",
        "country": "United Kingdom",
        "language": "en",
        "priority": 8,
        "reliability": 9,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://feeds.bbci.co.uk/news/politics/rss.xml"
    },

    {
        "id": "eu_politics",
        "name": "EU Politics",
        "category": "Politics",
        "region": "Europe",
        "country": "European Union",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/search?q=European+Union+politics&hl=en-US&gl=US&ceid=US:en"
    }

]