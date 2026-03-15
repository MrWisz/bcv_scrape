"""
Configuration for Swagger/OpenAPI documentation and rate limiting
"""

# Rate limits per endpoint group
RATE_LIMIT_SCRAPE = "30 per minute"    # endpoints that hit BCV website
RATE_LIMIT_P2P = "20 per minute"       # endpoints that hit Binance P2P
RATE_LIMIT_HISTORY = "60 per minute"   # endpoints that read local history file
RATE_LIMIT_HEALTH = "120 per minute"   # health/home endpoints

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "BCV Exchange Rate Scraper API",
        "description": "API for fetching Venezuelan exchange rates from BCV and Binance P2P USDT prices",
        "version": "1.0.0",
        "contact": {
            "name": "API Support"
        }
    },
    "schemes": ["https", "http"],
    "tags": [
        {
            "name": "Exchange Rates",
            "description": "BCV official exchange rates"
        },
        {
            "name": "P2P Prices",
            "description": "Binance P2P cryptocurrency prices"
        },
        {
            "name": "General",
            "description": "General API information"
        }
    ]
}
