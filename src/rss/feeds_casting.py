"""
LKS-HUB Casting RSS Feeds
"""

CASTING_FEEDS = [

    {
        "id": "google_news_casting",
        "name": "Google News Casting",
        "category": "Casting",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 7,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/search?q=casting+calls+film+television+actors&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "backstage_casting",
        "name": "Backstage Casting",
        "category": "Casting",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "casting_platform",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:backstage.com+casting&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "mandy_casting",
        "name": "Mandy Casting",
        "category": "Casting",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 7,
        "reliability": 7,
        "type": "casting_platform",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:mandy.com+casting&hl=en-US&gl=US&ceid=US:en"
    }

]