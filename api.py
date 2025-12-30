from flask import Flask, jsonify
from scrape_bcv import scrape_exchange_rates

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_rates():
    """
    Endpoint to get BCV exchange rates
    Returns JSON with USD and EUR rates
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
    Endpoint to get only USD rate
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
    Endpoint to get only EUR rate
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

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API documentation
    """
    return jsonify({
        'message': 'BCV Exchange Rate Scraper API',
        'endpoints': {
            '/rates': 'Get all exchange rates (USD and EUR)',
            '/rates/usd': 'Get only USD rate',
            '/rates/eur': 'Get only EUR rate'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
