from app.scraper.ebay import Ebay

e = Ebay('https://www.ebay.com/itm/186763637537')
r = e.get_reviews(10)
print(e.get_product_info())
print(r)
print(len(r))