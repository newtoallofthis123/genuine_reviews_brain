from app.scraper.utils import get_html
from bs4 import BeautifulSoup


class Amazon:
    @staticmethod
    def validate_amazon_url(url: str) -> bool:
        valid_domains = ['.com', '.in', '.co.uk']
        if not any('amazon' + domain in url for domain in valid_domains):
            return False
        return True

    @staticmethod
    def parse_product_id(url: str) -> str or None:
        parts = url.split('/')
        for part in parts:
            if 'B0' in part:
                return part

        return None

    @staticmethod
    def create_review_url(url: str) -> str:
        url = url.replace('dp', 'product-reviews')
        url += '?reviewerType=all_reviews'
        return url

    def get_review_url(self, page_number: int) -> str:
        return f'{self.review_url}&pageNumber={page_number}'

    def __init__(self, url):
        if not Amazon.validate_amazon_url(url):
            raise ValueError('Invalid Amazon URL')
        self.url = url
        self.pid = Amazon.parse_product_id(url)
        self.html = get_html(url)
        self.review_url = Amazon.create_review_url(url)
        self.page_number = 1
        self.b = BeautifulSoup(self.html, 'html.parser')

    def get_product_info(self) -> dict[str, str]:
        res = {}
        res['title'] = self.b.find('span', {'id': 'productTitle'}).text.strip()
        res['price'] = int(
            self.b.find('span', {'class': 'a-price-whole'}).text.strip().replace(',', '').replace('.', ''))
        res['discount'] = self.b.find('span', {'class': 'savingPriceOverride'}).text.strip()
        res['img'] = self.b.find('img', {'id': 'landingImage'})['src']

        return res

    def parse_review(self, page_number: int) -> list[dict[str, str]]:
        rb = BeautifulSoup(get_html("https://www.amazon.in/Apple-iPhone-Pro-Max-256/product-reviews/B0CHWWW471?reviewerType=all_reviews&pageNumber=2"), 'html.parser')
        rcon = rb.find_all('div', {'class': 'product-title'}, True)
        print(rcon)
        reviews = rb.find_all('div', {'data-hook': 'review'}, True)
        print(reviews)
        res = []
        for review in reviews:
            r = {}
            r['avatar'] = review.find('div', {'class': 'a-profile-avatar'}).find('img')['src']
            r['name'] = review.find('span', {'class': 'a-profile-name'}).text.strip()
            r['rating'] = float(review.find('i', {'data-hook': 'review-star-rating'}).text.strip().split(' ')[0])
            r['is_verified'] = review.find('span', {'data-hook': 'avp-badge'}) is not None
            r['title'] = review.find('a', {'data-hook': 'review-title'}).text.strip()
            r['review-date'] = review.find('span', {'data-hook': 'review-date'}).text.strip()
            r['body'] = review.find('span', {'data-hook': 'review-body'}).text.strip()
            res.append(r)

        return res

    def get_reviews(self, n: int = 20):
        return get_html(self.get_review_url(1))
