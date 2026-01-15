"""
Service for managing historical exchange rates
"""
import json
import os
from datetime import datetime


HISTORY_FILE = 'rates_history.json'


def get_history_file_path():
    """Get the absolute path to the history file"""
    # Store in the root directory of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, HISTORY_FILE)


def load_history():
    """
    Load rates history from JSON file

    Returns:
        dict: Dictionary with dates as keys and rates as values
    """
    file_path = get_history_file_path()

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
        return {}


def save_rate_to_history(date, usd, eur):
    """
    Save a rate entry to history

    Args:
        date (str): Date in format "DD Month YYYY" or any string format
        usd (str): USD rate
        eur (str): EUR rate
    """
    history = load_history()

    # Use the date as key
    history[date] = {
        'USD': usd,
        'EUR': eur,
        'timestamp': datetime.now().isoformat()
    }

    file_path = get_history_file_path()

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print(f"Rate saved to history: {date}")
    except Exception as e:
        print(f"Error saving to history: {e}")


def get_all_rates():
    """
    Get all historical rates

    Returns:
        dict: All rates with dates as keys
    """
    return load_history()


def get_rate_by_date(date):
    """
    Get rate for a specific date

    Args:
        date (str): Date to lookup

    Returns:
        dict: Rate data for that date or None
    """
    history = load_history()
    return history.get(date)


def get_latest_rate():
    """
    Get the most recent rate from history

    Returns:
        tuple: (date, rate_data) or (None, None)
    """
    history = load_history()

    if not history:
        return None, None

    # Sort by timestamp (most recent first)
    sorted_dates = sorted(
        history.items(),
        key=lambda x: x[1].get('timestamp', ''),
        reverse=True
    )

    if sorted_dates:
        return sorted_dates[0]

    return None, None


def get_available_dates():
    """
    Get list of all available dates in history

    Returns:
        list: List of date strings sorted by most recent first
    """
    history = load_history()

    # Sort by timestamp (most recent first)
    sorted_items = sorted(
        history.items(),
        key=lambda x: x[1].get('timestamp', ''),
        reverse=True
    )

    return [item[0] for item in sorted_items]


def get_usd_percentage_change():
    """
    Calculate the percentage change of USD rate from the last saved day

    Returns:
        dict: Contains previous_date, previous_rate, current_date, current_rate,
              percentage_change, and change_direction, or None if insufficient data
    """
    history = load_history()

    if len(history) < 2:
        return None

    # Sort by timestamp (most recent first)
    sorted_items = sorted(
        history.items(),
        key=lambda x: x[1].get('timestamp', ''),
        reverse=True
    )

    # Get the two most recent entries
    current_date, current_data = sorted_items[0]
    previous_date, previous_data = sorted_items[1]

    # Extract USD rates and convert from string format "123,45" to float
    current_usd_str = current_data.get('USD', '0')
    previous_usd_str = previous_data.get('USD', '0')

    # Remove commas and convert to float
    current_usd = float(current_usd_str.replace(',', '.'))
    previous_usd = float(previous_usd_str.replace(',', '.'))

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
