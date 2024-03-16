import time
import requests
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import logging

# Constants
TOR_PASSWORD = ""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}

# Setup logging
logging.basicConfig(level=logging.DEBUG)


# Tor session
def get_tor_session():
    tor = requests.session()
    # Tor uses the 9050 port as the default socks port
    tor.proxies = {'http': 'socks5://127.0.0.1:9050',
                   'https': 'socks5://127.0.0.1:9050'}
    return tor


session = get_tor_session()


def change_tor_identity():
    with Controller.from_port(port=9050) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())


def handle_captcha(response):
    # Check if response indicates CAPTCHA challenge
    if "captcha" in response.text.lower():
        # Here you would implement CAPTCHA solving logic
        logging.warning("CAPTCHA detected. Manual intervention required.")
        # For demonstration purposes, let's pause and wait for user input
        input("Please solve the CAPTCHA and press Enter to continue...")
        # Retry the request after CAPTCHA solved
        return True
    return False


def make_tor_request(url):
    try:
        response = session.get(url, verify=False, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if handle_captcha(response):
            # If CAPTCHA was detected and handled, retry the request
            return make_tor_request(url)
        return response
    except requests.RequestException as e:
        logging.error("Error occurred during request:", e)
        return None


def search_product(product_name):
    url = f"https://www.amazon.com/s?k={product_name}"
    response = make_tor_request(url)
    if response:
        raw_html = response.text
        # Parse HTML
        soup = BeautifulSoup(raw_html, "html.parser")
        logging.debug(soup.prettify())
        # Change Tor identity for next request
        change_tor_identity()


def scrape_product(product_id):
    url = f"https://www.amazon.com/dp/{product_id}/"
    response = make_tor_request(url)
    if response:
        raw_html = response.text
        # Parse HTML
        soup = BeautifulSoup(raw_html, "html.parser")
        logging.debug(soup.prettify())
        # Change Tor identity for next request
        change_tor_identity()
        product_title_element = soup.find('span', attrs={'id': 'productTitle'})
        if product_title_element:
            product_title = product_title_element.text.strip()
            return {"name": product_title}
        else:
            return {"result": "product title not found"}
