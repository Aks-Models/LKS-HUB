"""
LKS-HUB Science RSS Feeds
"""

SCIENCE_FEEDS = [

    {
        "id": "google_news_science",
        "name": "Google News Science",
        "category": "Science",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 9,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "science_daily",
        "name": "ScienceDaily",
        "category": "Science",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "science_media",
        "active": True,
        "url": "https://www.sciencedaily.com/rss/top/science.xml"
    },

    {
        "id": "phys_org",
        "name": "Phys.org",
        "category": "Science",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "science_media",
        "active": True,
        "url": "https://phys.org/rss-feed/"
    },

    {
        "id": "nature_news",
        "name": "Nature News",
        "category": "Science",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 9,
        "reliability": 9,
        "type": "science_journal_news",
        "active": True,
        "url": "https://www.nature.com/nature.rss"
    }

]