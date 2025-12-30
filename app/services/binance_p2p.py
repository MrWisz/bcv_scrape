"""
Service for fetching cryptocurrency prices from Binance P2P
"""
import requests


def get_binance_p2p_price(asset="USDT", fiat="VES", payment_methods=None):
    """
    Fetches the best buy price from Binance P2P marketplace

    Args:
        asset (str): The cryptocurrency asset (default: USDT)
        fiat (str): The fiat currency (default: VES)
        payment_methods (list): List of payment method codes to filter by (default: all methods)

    Returns:
        float: The best buy price, or None if failed
    """
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    payload = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": payment_methods or [],  # Empty for all payment methods
        "publisherType": None,
        "rows": 10,
        "tradeType": "BUY"  # "BUY" means you're buying USDT (sellers offering USDT)
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            ads = data.get("data", [])
            if ads:
                # Get the first (best) offer
                best_offer = ads[0]["adv"]
                price = float(best_offer["price"])
                return price

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Binance P2P price: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
