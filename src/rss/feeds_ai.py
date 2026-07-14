"""
LKS-HUB AI RSS Feeds
"""

AI_FEEDS = [

    {
        "id": "openai_news",
        "name": "OpenAI News",
        "category": "AI",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 10,
        "reliability": 10,
        "type": "official_company_news",
        "active": True,
        "url": "https://openai.com/news/rss.xml"
    },

    {
        "id": "google_news_ai",
        "name": "Google News AI",
        "category": "AI",
        "region": "Global",
        "country": "Global",
        "language": "en",
        "priority": 9,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://news.google.com/rss/search?q=artificial+intelligence+OR+AI+OR+machine+learning&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "mit_news_ai",
        "name": "MIT News Artificial Intelligence",
        "category": "AI",
        "region": "North America",
        "country": "United States",
        "language": "en",
        "priority": 9,
        "reliability": 9.5,
        "type": "academic_research_news",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:news.mit.edu+artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "venturebeat_ai",
        "name": "VentureBeat AI",
        "category": "AI",
        "region": "North America",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "technology_media",
        "active": True,
        "url": "https://venturebeat.com/category/ai/feed/"
    }

]