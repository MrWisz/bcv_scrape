"""
Service for managing historical exchange rates (MongoDB-backed)
"""
from datetime import datetime
from app.db import get_db

COLLECTION_NAME = 'rates_history'


def get_collection():
    """Get the MongoDB collection storing rate history"""
    return get_db()[COLLECTION_NAME]


def _to_entry(doc):
    """Strip the Mongo _id and shape a document like the old JSON value"""
    return {
        'USD': doc['USD'],
        'EUR': doc['EUR'],
        'timestamp': doc['timestamp']
    }


def save_rate_to_history(date, usd, eur):
    """
    Save a rate entry to history

    Args:
        date (str): Date in format "DD Month YYYY" or any string format
        usd (str): USD rate
        eur (str): EUR rate
    """
    try:
        collection = get_collection()
        collection.update_one(
            {'date': date},
            {'$set': {
                'USD': usd,
                'EUR': eur,
                'timestamp': datetime.now().isoformat()
            }},
            upsert=True
        )
        print(f"Rate saved to history: {date}")
    except Exception as e:
        print(f"Error saving to history: {e}")


def get_all_rates():
    """
    Get all historical rates

    Returns:
        dict: All rates with dates as keys
    """
    collection = get_collection()
    return {doc['date']: _to_entry(doc) for doc in collection.find()}


def get_rate_by_date(date):
    """
    Get rate for a specific date

    Args:
        date (str): Date to lookup

    Returns:
        dict: Rate data for that date or None
    """
    collection = get_collection()
    doc = collection.find_one({'date': date})
    return _to_entry(doc) if doc else None


def get_latest_rate():
    """
    Get the most recent rate from history

    Returns:
        tuple: (date, rate_data) or (None, None)
    """
    collection = get_collection()
    doc = collection.find_one(sort=[('timestamp', -1)])

    if not doc:
        return None, None

    return doc['date'], _to_entry(doc)


def get_available_dates():
    """
    Get list of all available dates in history

    Returns:
        list: List of date strings sorted by most recent first
    """
    collection = get_collection()
    return [doc['date'] for doc in collection.find(sort=[('timestamp', -1)])]


def get_usd_percentage_change():
    """
    Calculate the percentage change of USD rate from the last saved day

    Returns:
        dict: Contains previous_date, previous_rate, current_date, current_rate,
              percentage_change, and change_direction, or None if insufficient data
    """
    collection = get_collection()
    docs = list(collection.find(sort=[('timestamp', -1)], limit=2))

    if len(docs) < 2:
        return None

    current_data, previous_data = docs[0], docs[1]
    current_date, previous_date = current_data['date'], previous_data['date']

    # Remove commas and convert to float
    current_usd = float(current_data['USD'].replace(',', '.'))
    previous_usd = float(previous_data['USD'].replace(',', '.'))

    # Calculate percentage change: ((current - previous) / previous) * 100
    if previous_usd == 0:
        return None

    percentage_change = ((current_usd - previous_usd) / previous_usd) * 100

    # Truncate to 3 decimal places (not rounded)
    percentage_change = int(percentage_change * 1000) / 1000

    # Determine direction
    if percentage_change > 0:
        change_direction = "increase"
    elif percentage_change < 0:
        change_direction = "decrease"
    else:
        change_direction = "no change"

    return {
        'previous_date': previous_date,
        'previous_rate': previous_usd,
        'current_date': current_date,
        'current_rate': current_usd,
        'percentage_change': percentage_change,
        'change_direction': change_direction
    }
