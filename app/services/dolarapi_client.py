"""
Client for DolarAPI (https://dolarapi.com) - Venezuela exchange rates.

Replaces the BCV website scraper with a public API that already tracks
the official (BCV) rate and its full history. Binance P2P is still used
separately for the USDT rate (see app/services/binance_p2p.py).

DolarAPI documents no rate limit, but it's a free, unauthenticated public
API, so every call here is cached in-process to keep our own traffic to
it minimal regardless of how many requests our own API receives (see
app/services/ttl_cache.py for why a plain module-level cache is safe -
single gunicorn worker on Render).
"""
from datetime import datetime

import requests

from app.services.ttl_cache import TTLCache

BASE_URL = "https://ve.dolarapi.com/v1"

_MONTHS_ES = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]
_WEEKDAYS_ES = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
_MONTHS_ES_TO_NUM = {name: f"{i + 1:02d}" for i, name in enumerate(_MONTHS_ES)}

# History barely changes intraday (only "today" gets added once), so it's
# safe to cache for longer and cut request volume further.
_HISTORY_CACHE_TTL_SECONDS = 3 * 60 * 60
_history_cache = TTLCache(ttl_seconds=_HISTORY_CACHE_TTL_SECONDS)
_HISTORY_CACHE_KEY = 'official_history'


def _to_spanish_date(iso_or_datetime_str):
    """
    Format a date as "Miércoles, 17 Septiembre 2026" - matches BCV's own
    site formatting, which the calculator frontend still parses.
    """
    date_part = iso_or_datetime_str[:10]
    year, month, day = date_part.split('-')
    dt = datetime(int(year), int(month), int(day))
    return f"{_WEEKDAYS_ES[dt.weekday()]}, {day} {_MONTHS_ES[int(month) - 1]} {year}"


def _from_spanish_date(spanish_date):
    """Inverse of _to_spanish_date: "Miércoles, 17 Septiembre 2026" -> "2026-09-17\""""
    parts = spanish_date.split(' ')
    day = parts[1].zfill(2)
    month = _MONTHS_ES_TO_NUM[parts[2]]
    year = parts[3]
    return f"{year}-{month}-{day}"


def _format_rate(promedio):
    """Match BCV's own site formatting: comma decimal, 8 decimal places."""
    return f"{promedio:.8f}".replace('.', ',')


def get_official_rates():
    """
    Gets the current official (BCV) USD and EUR rates - the most recent
    entry in DolarAPI's own history.

    This deliberately reads history instead of DolarAPI's "current rate"
    endpoints (/cotizaciones, /dolares/oficial, /euros/oficial): those have
    been observed lagging days behind DolarAPI's own /historicos endpoints,
    which caused /rates to serve an older rate than /rates/history did.
    Reading both from the same history keeps them always in sync.

    Returns:
        dict: {'USD': str, 'EUR': str, 'date': str} or None if no history
    """
    history = _get_official_history()
    if not history:
        return None

    latest = history[-1]
    return {
        'USD': latest['USD'],
        'EUR': latest['EUR'],
        'date': _to_spanish_date(latest['date'])
    }


def _get_official_history():
    """Fetch (or return cached) full official-rate history, merged by date."""
    cached, is_fresh = _history_cache.get(_HISTORY_CACHE_KEY)
    if is_fresh:
        return cached

    try:
        usd_resp = requests.get(f"{BASE_URL}/historicos/dolares/oficial", timeout=15)
        usd_resp.raise_for_status()
        eur_resp = requests.get(f"{BASE_URL}/historicos/euros/oficial", timeout=15)
        eur_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching history from DolarAPI: {e}")
        return cached or []

    usd_by_date = {entry['fecha']: entry['promedio'] for entry in usd_resp.json()}
    eur_by_date = {entry['fecha']: entry['promedio'] for entry in eur_resp.json()}

    merged = [
        {
            'date': iso_date,
            'USD': _format_rate(usd_by_date[iso_date]),
            'EUR': _format_rate(eur_by_date[iso_date])
        }
        for iso_date in sorted(set(usd_by_date) & set(eur_by_date))
    ]

    _history_cache.set(_HISTORY_CACHE_KEY, merged)
    return merged


def get_all_rates():
    """
    Get all historical exchange rates.

    Returns:
        dict: Rates keyed by BCV-formatted date string
    """
    return {
        _to_spanish_date(entry['date']): {'USD': entry['USD'], 'EUR': entry['EUR']}
        for entry in _get_official_history()
    }


def get_available_dates():
    """
    Get list of all available dates in history.

    Returns:
        list: BCV-formatted date strings, most recent first
    """
    return [_to_spanish_date(entry['date']) for entry in reversed(_get_official_history())]


def get_rate_by_date(date):
    """
    Get rate for a specific date.

    Args:
        date (str): BCV-formatted date string (e.g. "Miércoles, 17 Septiembre 2026")

    Returns:
        dict: {'USD': str, 'EUR': str} or None if not found
    """
    iso_date = _from_spanish_date(date)
    return next(
        ({'USD': e['USD'], 'EUR': e['EUR']} for e in _get_official_history() if e['date'] == iso_date),
        None
    )


def get_usd_percentage_change():
    """
    Calculate the percentage change of USD rate from the last available day.

    Returns:
        dict: previous/current dates and rates plus percentage_change and
              change_direction, or None if insufficient data
    """
    history = _get_official_history()

    if len(history) < 2:
        return None

    current_data, previous_data = history[-1], history[-2]

    current_usd = float(current_data['USD'].replace(',', '.'))
    previous_usd = float(previous_data['USD'].replace(',', '.'))

    if previous_usd == 0:
        return None

    # Truncate to 3 decimal places (not rounded)
    percentage_change = int(((current_usd - previous_usd) / previous_usd) * 100 * 1000) / 1000

    if percentage_change > 0:
        change_direction = "increase"
    elif percentage_change < 0:
        change_direction = "decrease"
    else:
        change_direction = "no change"

    return {
        'previous_date': _to_spanish_date(previous_data['date']),
        'previous_rate': previous_usd,
        'current_date': _to_spanish_date(current_data['date']),
        'current_rate': current_usd,
        'percentage_change': percentage_change,
        'change_direction': change_direction
    }
