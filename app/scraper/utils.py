import requests

# Uses a standard Chrome user agent
HEADERS: dict[str, str] = ({'User-Agent':
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                            AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/90.0.4430.212 Safari/537.36',
                            'Accept-Language': 'en-US, en;q=0.5'})


def get_html(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """

    response = requests.get(url, headers=HEADERS)
    return response.text
