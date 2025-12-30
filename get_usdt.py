import requests

def get_binance_p2p_price():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],  # Empty for all payment methods
        "publisherType": None,
        "rows": 10,
        "tradeType": "BUY"  # "BUY" means you're buying USDT (sellers offering USDT)
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    if data.get("success"):
        ads = data.get("data", [])
        if ads:
            # Get the first (best) offer
            best_offer = ads[0]["adv"]
            price = float(best_offer["price"])
            return price
    
    return None

# Example usage
price = get_binance_p2p_price()
if price:
    print(f"Binance P2P USDT/VES buy price: {price:.2f} VES")
