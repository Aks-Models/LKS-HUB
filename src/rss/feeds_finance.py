"""
LKS-HUB Finance RSS Feeds
"""

FINANCE_FEEDS = [

    {
        "id": "marketwatch",
        "name": "MarketWatch Top Stories",
        "category": "Finance",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 10,
        "reliability": 9,
        "type": "financial_news",
        "active": True,
        "url": "https://feeds.content.dowjones.io/public/rss/mw_topstories"
    },

    {
        "id": "yahoo_finance",
        "name": "Yahoo Finance",
        "category": "Finance",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "financial_news",
        "active": True,
        "url": "https://finance.yahoo.com/rss/topstories"
    },

    {
        "id": "cnbc_finance",
        "name": "CNBC Finance",
        "category": "Finance",
        "region": "Global",
        "country": "United States",
        "language": "en",
        "priority": 9,
        "reliability": 9,
        "type": "financial_news",
        "active": True,
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    }

]