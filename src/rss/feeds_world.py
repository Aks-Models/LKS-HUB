"""
LKS-HUB World RSS Feeds

Trusted global news sources used by the LKS-HUB Intelligence Engine.
"""

WORLD_FEEDS = [

    {
        "id": "bbc_world",
        "name": "BBC World",
        "category": "World",
        "region": "Europe",
        "country": "United Kingdom",
        "language": "en",
        "priority": 10,
        "reliability": 9.5,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml"
    },

    {
        "id": "reuters_world",
        "name": "Reuters World",
        "category": "World",
        "region": "Global",
        "country": "United Kingdom",
        "language": "en",
        "priority": 10,
        "reliability": 10,
        "type": "news_agency",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:reuters.com/world/+when:1h&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "associated_press_top",
        "name": "Associated Press Top News",
        "category": "World",
        "region": "North America",
        "country": "United States",
        "language": "en",
        "priority": 10,
        "reliability": 9.8,
        "type": "news_agency",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:apnews.com/world&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "al_jazeera_english",
        "name": "Al Jazeera English",
        "category": "World",
        "region": "Middle East",
        "country": "Qatar",
        "language": "en",
        "priority": 9,
        "reliability": 8.5,
        "type": "broadcaster",
        "active": True,
        "url": "https://www.aljazeera.com/xml/rss/all.xml"
    },

    {
        "id": "dw_english",
        "name": "Deutsche Welle English",
        "category": "World",
        "region": "Europe",
        "country": "Germany",
        "language": "en",
        "priority": 9,
        "reliability": 9,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://rss.dw.com/xml/rss-en-all"
    },

    {
        "id": "france24_english",
        "name": "France 24 English",
        "category": "World",
        "region": "Europe",
        "country": "France",
        "language": "en",
        "priority": 8,
        "reliability": 8.8,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://www.france24.com/en/rss"
    },

    {
        "id": "cgtn_world",
        "name": "CGTN World",
        "category": "World",
        "region": "Asia",
        "country": "China",
        "language": "en",
        "priority": 8,
        "reliability": 7,
        "type": "state_broadcaster",
        "active": False,
        "url": "https://www.cgtn.com/subscribe/rss.html"
    },

    {
        "id": "abc_australia",
        "name": "ABC Australia",
        "category": "World",
        "region": "Oceania",
        "country": "Australia",
        "language": "en",
        "priority": 8,
        "reliability": 9,
        "type": "public_broadcaster",
        "active": True,
        "url": "https://www.abc.net.au/news/feed/51120/rss.xml"
    },

    {
        "id": "allafrica",
        "name": "AllAfrica",
        "category": "World",
        "region": "Africa",
        "country": "Pan-African",
        "language": "en",
        "priority": 8,
        "reliability": 8,
        "type": "news_aggregator",
        "active": True,
        "url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"
    },

    {
        "id": "indian_express",
        "name": "The Indian Express",
        "category": "World",
        "region": "Asia",
        "country": "India",
        "language": "en",
        "priority": 8,
        "reliability": 8.5,
        "type": "newspaper",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:indianexpress.com/section/world&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "tass_world",
        "name": "TASS World",
        "category": "World",
        "region": "Europe",
        "country": "Russia",
        "language": "en",
        "priority": 8,
        "reliability": 7,
        "type": "state_news_agency",
        "active": True,
        "url": "https://tass.com/rss/v2.xml"
    },

    {
        "id": "wafa_english",
        "name": "WAFA English",
        "category": "World",
        "region": "Middle East",
        "country": "Palestine",
        "language": "en",
        "priority": 8,
        "reliability": 7.5,
        "type": "state_news_agency",
        "active": True,
        "url": "https://news.google.com/rss/search?q=site:english.wafa.ps&hl=en-US&gl=US&ceid=US:en"
    },

    {
        "id": "irna_english",
        "name": "IRNA English",
        "category": "World",
        "region": "Middle East",
        "country": "Iran",
        "language": "en",
        "priority": 8,
        "reliability": 7,
        "type": "state_news_agency",
        "active": True,
        "url": "https://en.irna.ir/rss"
    }

]