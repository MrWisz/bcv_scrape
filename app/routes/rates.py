"""
Routes for BCV exchange rate endpoints
"""
from flask import Blueprint, jsonify
from app.services.bcv_scraper import scrape_exchange_rates

rates_bp = Blueprint('rates', __name__, url_prefix='/rates')


@rates_bp.route('/', methods=['GET'])
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


@rates_bp.route('/usd', methods=['GET'])
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


@rates_bp.route('/eur', methods=['GET'])
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


@rates_bp.route('/date', methods=['GET'])
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
