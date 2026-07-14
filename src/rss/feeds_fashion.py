"""
LKS-HUB Fashion RSS Feeds
"""

FASHION_FEEDS = [

    {
        "id": "google_news_fashion",
        "name": "Google News Fashion",
        "category": "Fashion",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 7,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/search?q=fashion+industry+OR+luxury+fashion&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "vogue_business",
        "name": "Vogue Business",
        "category": "Fashion",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "fashion_business_media",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:voguebusiness.com&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "business_of_fashion",
        "name": "Business of Fashion",
        "category": "Fashion",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "fashion_business_media",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:businessoffashion.com&hl=en-US&gl=US&ceid=US:en"
    }

]