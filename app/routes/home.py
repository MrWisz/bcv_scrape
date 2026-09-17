"""
Routes for general API information
"""
from flask import Blueprint, jsonify
from app.extensions import limiter
from app.config import RATE_LIMIT_HEALTH
from app.auth import require_api_key

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
@limiter.limit(RATE_LIMIT_HEALTH)
@require_api_key
def home():
    """
    API Home
    ---
    tags:
      - General
    security:
      - ApiKeyAuth: []
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
              example: "Venezuela Exchange Rate API"
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
                /rates/usd/paralelo:
                  type: string
                  example: "Get the USD parallel (non-official) exchange rate"
            documentation:
              type: string
              example: "Visit /docs for interactive API documentation"
    """
    return jsonify({
        'message': 'Venezuela Exchange Rate API',
        'endpoints': {
            '/rates': 'Get all exchange rates (USD, EUR, and date)',
            '/rates/usd': 'Get only USD rate',
            '/rates/eur': 'Get only EUR rate',
            '/rates/date': 'Get the applicable date for the rates',
            '/rates/usd/paralelo': 'Get the USD parallel (non-official) exchange rate'
        },
        'documentation': 'Visit /docs for interactive API documentation'
    }), 200
