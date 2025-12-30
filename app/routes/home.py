"""
Routes for general API information
"""
from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
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
