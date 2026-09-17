"""
Service for scraping exchange rates from Banco Central de Venezuela
"""
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from lxml import html
import urllib3
from app.services.rates_history import save_rate_to_history
from app.services.ttl_cache import TTLCache

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Short TTL just to avoid re-scraping bcv.org.ve on every single request.
# The real "has BCV published a new rate" check is the Caracas calendar-day
# comparison below - BCV updates once a day at no fixed time, so a flat
# rolling TTL (e.g. 24h since last scrape) can stay "fresh" well past the
# moment BCV actually publishes the new day's rate.
_CACHE_TTL_SECONDS = 30 * 60
_cache = TTLCache(ttl_seconds=_CACHE_TTL_SECONDS)
_CACHE_KEY = 'bcv_rates'
_CARACAS_TZ = ZoneInfo("America/Caracas")
_cached_day = None


def scrape_exchange_rates():
    """
    Scrapes exchange rates from Banco Central de Venezuela website.
    Cached briefly to avoid re-scraping bcv.org.ve on every request, but
    always re-scrapes once the Caracas calendar day rolls over so a new
    BCV-published rate isn't masked by a stale cache entry.

    Returns:
        dict: Dictionary containing USD, EUR rates and date, or None if failed
    """
    global _cached_day

    current_day = datetime.now(_CARACAS_TZ).date()
    cached_rates, is_fresh = _cache.get(_CACHE_KEY)
    if is_fresh and _cached_day == current_day:
        return cached_rates

    url = "https://www.bcv.org.ve/"

    try:
        # Send GET request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()

        # Parse the HTML content
        tree = html.fromstring(response.content)

        # Extract the USD value using XPath
        usd_xpath = '/html/body/div[4]/div/div[2]/div/div[1]/div[1]/section[1]/div/div[2]/div/div[7]/div/div/div[2]/strong'
        usd_element = tree.xpath(usd_xpath)

        # Extract the EUR value using XPath
        eur_xpath = '/html/body/div[4]/div/div[2]/div/div[1]/div[1]/section[1]/div/div[2]/div/div[3]/div/div/div[2]/strong'
        eur_element = tree.xpath(eur_xpath)

        # Extract the date using XPath
        date_xpath = '/html/body/div[4]/div/div[2]/div/div[1]/div[1]/section[1]/div/div[2]/div/div[8]/span'
        date_element = tree.xpath(date_xpath)

        rates = {}

        if usd_element:
            usd_rate = usd_element[0].text_content().strip()
            rates['USD'] = usd_rate

        if eur_element:
            eur_rate = eur_element[0].text_content().strip()
            rates['EUR'] = eur_rate

        if date_element:
            date = date_element[0].text_content().strip()
            # Remove extra spaces (normalize multiple spaces to single space)
            date = ' '.join(date.split())
            rates['date'] = date

        # Save to history if we have all the data
        if rates and 'USD' in rates and 'EUR' in rates and 'date' in rates:
            save_rate_to_history(rates['date'], rates['USD'], rates['EUR'])
            _cache.set(_CACHE_KEY, rates)
            _cached_day = current_day
            return rates

        # Incomplete scrape - fall back to stale cache rather than failing outright
        return cached_rates

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return cached_rates
    except Exception as e:
        print(f"An error occurred: {e}")
        return cached_rates
