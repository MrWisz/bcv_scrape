"""
Service for fetching cryptocurrency prices from Binance P2P
"""
import requests


def get_binance_p2p_price(asset="USDT", fiat="VES", payment_methods=None, num_prices=50, min_trades=1000, min_completion_rate=98.0):
    """
    Fetches the average buy price from Binance P2P marketplace

    Args:
        asset (str): The cryptocurrency asset (default: USDT)
        fiat (str): The fiat currency (default: VES)
        payment_methods (list): List of payment method codes to filter by (default: all methods)
        num_prices (int): Number of prices to average (default: 300)
        min_trades (int): Minimum number of trades required (default: 1000)
        min_completion_rate (float): Minimum 30-day completion rate required (default: 98.0)

    Returns:
        float: The average buy price, or None if failed
    """
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    headers = {
        "Content-Type": "application/json"
    }

    all_prices = []
    max_rows_per_page = 20  # Binance API limit

    try:
        page = 1
        # Keep fetching until we have enough qualifying prices
        while len(all_prices) < num_prices:
            payload = {
                "asset": asset,
                "fiat": fiat,
                "merchantCheck": True,
                "page": page,
                "payTypes": payment_methods or [],  # Empty for all payment methods
                "publisherType": None,
                "rows": max_rows_per_page,
                "tradeType": "BUY"  # "BUY" means you're buying USDT (sellers offering USDT)
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                ads = data.get("data", [])
                if not ads:
                    # No more ads available
                    break

                # Filter ads based on merchant criteria
                for ad in ads:
                    if len(all_prices) >= num_prices:
                        break

                    try:
                        advertiser = ad.get("advertiser", {})
                        # Check if merchant meets requirements
                        # monthFinishRate is a percentage (0-1), convert to 0-100 scale
                        month_finish_rate = float(advertiser.get("monthFinishRate", 0)) * 100
                        month_order_count = int(advertiser.get("monthOrderCount", 0))

                        # Only include if meets minimum requirements
                        if month_order_count >= min_trades and month_finish_rate >= min_completion_rate:
                            price = float(ad["adv"]["price"])
                            all_prices.append(price)
                    except (KeyError, ValueError, TypeError) as e:
                        # Skip this ad if data is malformed
                        print(f"Skipping ad due to data error: {e}")
                        continue
            else:
                break

            page += 1
            # Safety limit to prevent infinite loops
            if page > 100:
                break

        if all_prices:
            # Calculate and return the average
            average_price = sum(all_prices) / len(all_prices)
            # Truncate to 3 decimal places
            average_price = int(average_price * 1000) / 1000
            print(f"Successfully collected {len(all_prices)} prices from qualifying sellers")
            return average_price

        print(f"No qualifying sellers found with criteria: {min_trades}+ trades, {min_completion_rate}%+ completion rate")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Binance P2P price: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
