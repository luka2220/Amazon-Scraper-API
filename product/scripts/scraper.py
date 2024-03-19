import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 '
                  'Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Setup logging
logging.basicConfig(level=logging.DEBUG)


def search_product(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    response = requests.get(url, headers=HEADERS)
    if response:
        raw_html = response.text
        soup = BeautifulSoup(raw_html, "lxml")


def scrape_product(product_id):
    # TODO => Convert block to a try/catch for better error handling

    url = f"https://www.amazon.com/dp/{product_id}/"

    # response = make_tor_request(url)
    response = requests.get(url, headers=HEADERS)

    if response:
        raw_html = response.text
        # Parse HTML
        soup = BeautifulSoup(raw_html, "lxml")

        # Extract product title
        try:
            product_title_element = soup.select_one('#productTitle')
            product_title = product_title_element.text.strip()
        except AttributeError:
            product_title = ''

        # Extract product price
        selectors = ['span.aok-offscreen', 'span.a-price-whole', 'span.a-offscreen']
        product_price = None

        for selector in selectors:
            element = soup.select_one(selector)
            if element and len(element.text) <= 10:
                if '$' in element.text:
                    product_price = element.text.strip()[1:]
                else:
                    product_price = element.text.strip()

                if product_price[-1] == '.':
                    product_price += '00'

                break

        # Extract sale data

        try:
            rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

        except AttributeError:

            try:
                rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
            except AttributeError:
                rating = ""

        try:
            review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
        except AttributeError:
            review_count = ""

        try:
            available = soup.find("div", attrs={'id': 'availability'})
            available = available.find("span").string.strip()
        except AttributeError:
            available = ""

        # Extract product info
        product_info = {}
        product_data = soup.select('tr.a-spacing-small')

        for element in product_data:
            td_elements = element.find_all('td')

            if len(td_elements) == 2:
                key = td_elements[0].text.strip()
                value = td_elements[1].text.strip()

                product_info[key] = value

        product_sale_info = {
            "available": available,
            "num_reviews": review_count,
            "ratings": rating
        }

        return {
            "id": product_id,
            "title": product_title,
            "price": product_price,
            "info": product_info,
            "sale_data": product_sale_info,
        }
    else:
        print('Response failed...')
