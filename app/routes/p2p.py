"""
Routes for Binance P2P cryptocurrency price endpoints
"""
from flask import Blueprint, jsonify
from app.services.binance_p2p import get_binance_p2p_price

p2p_bp = Blueprint('p2p', __name__, url_prefix='/p2p')


@p2p_bp.route('/usdt', methods=['GET'])
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
