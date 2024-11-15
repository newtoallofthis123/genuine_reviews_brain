# List of all the valid sites supported by the parser
import re

VALID_SITES = [
    'amazon',
    'bestbuy',
    'flipkart',
    'ebay'
]


def is_valid_url(url):
    """
    Checks if a given URL is valid.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    pattern = r'^(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)*/?$'
    if re.match(pattern, url):
        return True
    else:
        return False


def parse_site(url: str) -> str or None:
    """
    Parses the site name from the url and checks if it is supported

    Args:
    url (str): The url of the site

    Returns:
    str: The site name if it is supported, otherwise None
    """
    if not url:
        return None

    if not is_valid_url(url):
        return None

    for site in VALID_SITES:
        if site in url:
            return site

    return None


def scrape(url: str, n: int = 20) -> list[str] or None:
    site = parse_site(url)
    if not site:
        return None

    if site == 'amazon':
        from .amazon import Amazon
        a = Amazon(url)
        return a.get_reviews(n)
    elif site == 'ebay':
        from .ebay import Ebay

        e = Ebay(url)
        r = e.get_product_info()
        r['reviews'] = e.get_reviews(n)
        return r
    else:
        return None
