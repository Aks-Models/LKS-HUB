"""
LKS-HUB Business RSS Feeds
"""

BUSINESS_FEEDS = [

    {
        "id": "bbc_business",
        "name": "BBC Business",
        "category": "Business",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 9,
        "reliability": 9,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml"
    },

    {
        "id": "google_news_business",
        "name": "Google News Business",
        "category": "Business",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en"
    }

]