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
    # response = make_tor_request(url)
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
        product_title_element = soup.select_one('#productTitle')
        product_title = product_title_element.text.strip()

        # Extract product price
        selectors = ['span.aok-offscreen', 'span.a-offscreen']
        product_price = None

        for selector in selectors:
            product_price_element = soup.select_one(selector)
            if product_price_element:
                product_price = product_price_element.text.strip()[1:]
                break

        # Extract product info
        product_info_elements_titles = soup.select('th.prodDetSectionEntry')
        product_info_elements_values = soup.select('td.prodDetAttrValue')

        product_info = {}

        for i in range(len(product_info_elements_titles) - 3):
            title = product_info_elements_titles[i]
            value = product_info_elements_values[i]

            product_info[title.text.strip()] = value.text.strip()

        return {
            "id": product_id,
            "title": product_title,
            "price": product_price,
            "info": product_info
        }
