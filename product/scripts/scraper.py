import requests
from bs4 import BeautifulSoup

# testing site => https://www.amazon.com/dp/B0C5L9Z2Y1/

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/62.0.3202.94 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
}


def search_product(product_name):
    # TODO => product_name cannot have spaces
    # TODO => 'coffee maker' must be 'coffee+maker' in the request url

    url = f"https://www.amazon.com/s?k={product_name}"
    response = requests.get(url, headers=HEADERS)
    raw_html = response.text

    # remove all the <script> and <style> tage from document
    clean_html = BeautifulSoup(raw_html, "html.parser")
    for script in clean_html(["script", "style"]):
        script.decompose()

    soup = BeautifulSoup(str(clean_html), "html.parser")
    print(soup.prettify())


def scrape_product(product_id):
    url = f"https://www.amazon.com/dp/{product_id}/"
    response = requests.get(url, headers=HEADERS)
    raw_html = response.text

    # remove all the <script> and <style> tage from document
    clean_html = BeautifulSoup(raw_html, "html.parser")
    for script in clean_html(["script", "style"]):
        script.decompose()

    soup = BeautifulSoup(str(clean_html), "html.parser")

    product_title = soup.find('span', attrs={'id': 'productTitle'}).text

    # print(soup.prettify())
    # print(product_title)

    return {"name": product_title}
