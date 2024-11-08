from app.scraper.utils import get_html
from bs4 import BeautifulSoup

EBAY_FEEDBACK_URL = 'https://www.ebay.com/fdbk/mweb_profile?fdbkType=FeedbackReceivedAsSeller&'


class Ebay:
    @staticmethod
    def clean_url(url: str) -> str:
        """
        Cleans the URL by removing all query parameters and trailing slashes.
        """
        return url.split('?')[0].rstrip('/')

    def parse_pid(self) -> str or None:
        """
        Parses the product ID from the URL.
        """
        parts = self.url.split('/')[-1]
        if parts.isnumeric():
            return parts
        else:
            return None

    def parse_product_info(self) -> dict[str, str]:
        """
        Parses the product information from the HTML.

        Returns:
            dict[str, str]: A dictionary containing the following
                keys:
                - title: The title of the product.
                - price: The price of the product.
                - seller: The name of the seller.
                - img: The URL of the product image.
        """

        title = self.b.find('div', {'class': 'x-item-title'}).text.strip()
        price = self.b.find('div', {'data-testid': 'x-price-primary'}).text.strip()
        seller = self.b.find('h2', {'class': 'x-store-information__store-name'}).text.strip()
        img = self.b.find('div', {'class': 'ux-image-carousel-item'}).find('img')['src']

        return {
            'title': title,
            'price': price,
            'seller': seller,
            'img': img
        }

    def get_product_info(self):
        """Returns the product information."""
        return self.product

    def construct_reviews_url(self, page: int) -> str:
        """
        Constructs the URL for the reviews of the product.
        Uses the product ID and the seller name to construct the URL.
        """

        url = EBAY_FEEDBACK_URL + f'item={self.pid}&username={self.product['seller']}&sort=RELEVANCE&entries_per_page=25&page_id={page}'
        return url

    def get_reviews(self, n: int = 20) -> list[dict[str, str]]:
        """
        Returns the reviews of the product.
        This function will only work if the product has been parsed successfully in the constructor.

        Parameters:
            n (int): The minimum number of reviews to return.
            Most of the time, the number of reviews returned will be greater than n.

        Returns:
            list[dict[str, str]]: A list of reviews where each review is a dictionary containing the following keys:
                - body: The body of the review.
        """

        res = []
        page = self.page

        while len(res) < n:
            page += 1
            url = self.construct_reviews_url(page)
            html = get_html(url)
            rb = BeautifulSoup(html, 'html.parser')

            containers = rb.find_all('li', {'data-testid': 'feedback-cards'})

            for container in containers:
                r = {}
                r['body'] = container.find('div', {'class': 'fdbk-container__details__comment'}, True).text.strip()

                res.append(r)

        self.page = page

        return res

    def __init__(self, url):
        """
        Initializes the Ebay scraper.
        Calling it entails a connection to the URL as well as the parsing of the product information.
        This information can then be accessed using the get_product_info() method.

        Parameters:
            url (str): The URL of the product.
            This is stored without any query parameters or trailing slashes.

        Raises:
            ValueError: If the URL is invalid.

        Returns:
            None
        """

        self.url = Ebay.clean_url(url)
        self.html = get_html(url)
        self.b = BeautifulSoup(self.html, 'html.parser')
        self.product = self.parse_product_info()
        self.pid = self.parse_pid()
        self.page = 0
        if not self.pid:
            raise ValueError('Invalid URL')
