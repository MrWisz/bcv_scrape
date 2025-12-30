from flask import Flask, jsonify
from flasgger import Swagger
from scrape_bcv import scrape_exchange_rates
from get_usdt import get_binance_p2p_price

app = Flask(__name__)

# Swagger configuration
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
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.route('/rates', methods=['GET'])
def get_rates():
    """
    Get all BCV exchange rates
    ---
    tags:
      - Exchange Rates
    summary: Get all exchange rates (USD, EUR, and date)
    description: Retrieves the official exchange rates from Banco Central de Venezuela (BCV) for USD and EUR, along with the applicable date.
    responses:
      200:
        description: Successfully retrieved exchange rates
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                USD:
                  type: number
                  example: 36.50
                  description: USD to VES exchange rate
                EUR:
                  type: number
                  example: 39.75
                  description: EUR to VES exchange rate
                date:
                  type: string
                  example: "2025-12-30"
                  description: Date the rates are applicable
      500:
        description: Failed to scrape exchange rates
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to scrape exchange rates"
    """
    rates = scrape_exchange_rates()

    if rates:
        return jsonify({
            'success': True,
            'data': rates
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to scrape exchange rates'
        }), 500

@app.route('/rates/usd', methods=['GET'])
def get_usd_rate():
    """
    Get USD exchange rate
    ---
    tags:
      - Exchange Rates
    summary: Get only USD exchange rate
    description: Retrieves the official USD to VES exchange rate from Banco Central de Venezuela (BCV).
    responses:
      200:
        description: Successfully retrieved USD rate
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            currency:
              type: string
              example: "USD"
            rate:
              type: number
              example: 36.50
              description: USD to VES exchange rate
      500:
        description: Failed to scrape USD rate
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to scrape USD rate"
    """
    rates = scrape_exchange_rates()

    if rates and 'USD' in rates:
        return jsonify({
            'success': True,
            'currency': 'USD',
            'rate': rates['USD']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to scrape USD rate'
        }), 500

@app.route('/rates/eur', methods=['GET'])
def get_eur_rate():
    """
    Get EUR exchange rate
    ---
    tags:
      - Exchange Rates
    summary: Get only EUR exchange rate
    description: Retrieves the official EUR to VES exchange rate from Banco Central de Venezuela (BCV).
    responses:
      200:
        description: Successfully retrieved EUR rate
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            currency:
              type: string
              example: "EUR"
            rate:
              type: number
              example: 39.75
              description: EUR to VES exchange rate
      500:
        description: Failed to scrape EUR rate
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to scrape EUR rate"
    """
    rates = scrape_exchange_rates()

    if rates and 'EUR' in rates:
        return jsonify({
            'success': True,
            'currency': 'EUR',
            'rate': rates['EUR']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to scrape EUR rate'
        }), 500

@app.route('/rates/date', methods=['GET'])
def get_date():
    """
    Get exchange rates date
    ---
    tags:
      - Exchange Rates
    summary: Get the applicable date for the exchange rates
    description: Retrieves the date when the BCV exchange rates were published or are applicable.
    responses:
      200:
        description: Successfully retrieved date
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            date:
              type: string
              example: "2025-12-30"
              description: The date the rates are applicable
      500:
        description: Failed to scrape date
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to scrape date"
    """
    rates = scrape_exchange_rates()

    if rates and 'date' in rates:
        return jsonify({
            'success': True,
            'date': rates['date']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to scrape date'
        }), 500

@app.route('/p2p/usdt', methods=['GET'])
def get_usdt_p2p():
    """
    Get Binance P2P USDT/VES price
    ---
    tags:
      - P2P Prices
    summary: Get Binance P2P USDT/VES buy price
    description: Retrieves the current best buy price for USDT in VES from Binance P2P marketplace. This represents the price at which sellers are offering USDT.
    responses:
      200:
        description: Successfully retrieved USDT P2P price
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            currency:
              type: string
              example: "USDT"
              description: The cryptocurrency being traded
            fiat:
              type: string
              example: "VES"
              description: The fiat currency
            price:
              type: number
              example: 36.85
              description: Current buy price for 1 USDT in VES
            source:
              type: string
              example: "Binance P2P"
              description: The source of the price data
      500:
        description: Failed to fetch Binance P2P price
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Failed to fetch Binance P2P price"
    """
    price = get_binance_p2p_price()

    if price:
        return jsonify({
            'success': True,
            'currency': 'USDT',
            'fiat': 'VES',
            'price': price,
            'source': 'Binance P2P'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch Binance P2P price'
        }), 500

@app.route('/', methods=['GET'])
def home():
    """
    API Home
    ---
    tags:
      - General
    summary: API information and available endpoints
    description: Returns basic information about the API and a list of available endpoints. For interactive documentation, visit /docs
    responses:
      200:
        description: API information
        schema:
          type: object
          properties:
            message:
              type: string
              example: "BCV Exchange Rate Scraper API"
            endpoints:
              type: object
              properties:
                /rates:
                  type: string
                  example: "Get all exchange rates (USD, EUR, and date)"
                /rates/usd:
                  type: string
                  example: "Get only USD rate"
                /rates/eur:
                  type: string
                  example: "Get only EUR rate"
                /rates/date:
                  type: string
                  example: "Get the applicable date for the rates"
                /p2p/usdt:
                  type: string
                  example: "Get Binance P2P USDT/VES buy price"
            documentation:
              type: string
              example: "Visit /docs for interactive API documentation"
    """
    return jsonify({
        'message': 'BCV Exchange Rate Scraper API',
        'endpoints': {
            '/rates': 'Get all exchange rates (USD, EUR, and date)',
            '/rates/usd': 'Get only USD rate',
            '/rates/eur': 'Get only EUR rate',
            '/rates/date': 'Get the applicable date for the rates',
            '/p2p/usdt': 'Get Binance P2P USDT/VES buy price'
        },
        'documentation': 'Visit /docs for interactive API documentation'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
