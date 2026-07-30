"""
Service for scraping exchange rates from Banco Central de Venezuela
"""
import requests
from lxml import html
import urllib3
from app.services.rates_history import save_rate_to_history
from app.services.ttl_cache import TTLCache

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# BCV only publishes new rates once a day; matches the external refresh cadence
_CACHE_TTL_SECONDS = 24 * 60 * 60
_cache = TTLCache(ttl_seconds=_CACHE_TTL_SECONDS)
_CACHE_KEY = 'bcv_rates'


def scrape_exchange_rates():
    """
    Scrapes exchange rates from Banco Central de Venezuela website.
    Cached for 24 hours to avoid re-scraping bcv.org.ve on every request.

    Returns:
        dict: Dictionary containing USD, EUR rates and date, or None if failed
    """
    cached_rates, is_fresh = _cache.get(_CACHE_KEY)
    if is_fresh:
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
            return rates

        # Incomplete scrape - fall back to stale cache rather than failing outright
        return cached_rates

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return cached_rates
    except Exception as e:
        print(f"An error occurred: {e}")
        return cached_rates
