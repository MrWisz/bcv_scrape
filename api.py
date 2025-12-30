from flask import Flask, jsonify
from scrape_bcv import scrape_exchange_rates
from get_usdt import get_binance_p2p_price

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_rates():
    """
    Endpoint to get BCV exchange rates
    Returns JSON with USD, EUR rates and the applicable date
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

@app.route('/rates/date', methods=['GET'])
def get_date():
    """
    Endpoint to get the applicable date for the exchange rates
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
    Endpoint to get Binance P2P USDT/VES buy price
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
    Home endpoint with API documentation
    """
    return jsonify({
        'message': 'BCV Exchange Rate Scraper API',
        'endpoints': {
            '/rates': 'Get all exchange rates (USD, EUR, and date)',
            '/rates/usd': 'Get only USD rate',
            '/rates/eur': 'Get only EUR rate',
            '/rates/date': 'Get the applicable date for the rates',
            '/p2p/usdt': 'Get Binance P2P USDT/VES buy price'
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
