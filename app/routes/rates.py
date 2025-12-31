"""
Routes for BCV exchange rate endpoints
"""
from flask import Blueprint, jsonify, request
from app.services.bcv_scraper import scrape_exchange_rates
from app.services.rates_history import get_all_rates, get_rate_by_date, get_available_dates

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


@rates_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get historical exchange rates
    ---
    tags:
      - Exchange Rates
    summary: Get all historical exchange rates
    description: Retrieves all saved historical exchange rates from the database.
    responses:
      200:
        description: Successfully retrieved history
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              description: Object with dates as keys and rate data as values
    """
    history = get_all_rates()

    return jsonify({
        'success': True,
        'data': history
    }), 200


@rates_bp.route('/history/dates', methods=['GET'])
def get_dates():
    """
    Get available dates in history
    ---
    tags:
      - Exchange Rates
    summary: Get list of available dates
    description: Retrieves a list of all dates that have saved exchange rates.
    responses:
      200:
        description: Successfully retrieved available dates
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            dates:
              type: array
              items:
                type: string
              example: ["Lunes, 30 Diciembre 2025", "Viernes, 27 Diciembre 2025"]
    """
    dates = get_available_dates()

    return jsonify({
        'success': True,
        'dates': dates
    }), 200


@rates_bp.route('/history/<date>', methods=['GET'])
def get_historical_rate(date):
    """
    Get exchange rate for specific date
    ---
    tags:
      - Exchange Rates
    summary: Get rate for a specific date
    description: Retrieves the exchange rate for a specific date from history.
    parameters:
      - name: date
        in: path
        required: true
        type: string
        description: The date to lookup (e.g. "Lunes, 30 Diciembre 2025")
    responses:
      200:
        description: Successfully retrieved rate
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            date:
              type: string
              example: "Lunes, 30 Diciembre 2025"
            data:
              type: object
              properties:
                USD:
                  type: string
                  example: "36,50"
                EUR:
                  type: string
                  example: "39,75"
      404:
        description: No data found for this date
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "No data found for this date"
    """
    rate_data = get_rate_by_date(date)

    if rate_data:
        return jsonify({
            'success': True,
            'date': date,
            'data': {
                'USD': rate_data['USD'],
                'EUR': rate_data['EUR']
            }
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'No data found for this date'
        }), 404
