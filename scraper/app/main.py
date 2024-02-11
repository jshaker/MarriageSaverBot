import logging
import json
from functools import partial
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
import undetected_chromedriver as uc

hostName = "localhost"
serverPort = 8080

def new_driver():
    _chrome_options = Options()  
    _chrome_options.add_argument("--disable-gpu")  # required for dockerized Chrome
    _chrome_options.add_argument("--headless")
    _chrome_options.add_argument("--incognito")  # optional
    _chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )  # any reasonable user agent will do

    # _chrome_options.add_argument("--no-sandbox")
    # _chrome_options.add_argument("--disable-setuid-sandbox")
    # _chrome_options.add_argument("--disable-extensions")
    # _chrome_options.add_argument('--disable-application-cache')
    # _chrome_options.add_argument('--disable-gpu')
    # _chrome_options.add_argument("--disable-setuid-sandbox")
    # _chrome_options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(headless=True, options=_chrome_options, use_subprocess=True)    
    return driver
    
class ProductPageScraper():
    def __init__(self, driver):
        self.driver = driver
    
    def get_price(self, url):
        # validate that URL is a valid Westelm product page
        if not url.startswith('https://www.westelm.com/products/'):
            return -1
         
        # navigate to the URL
        self.driver.get(url)

        # Check if request was blocked
        if '403' in self.driver.title:
            return -1
        
        # wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pip-river-container-WE > div.product-info-rvi > div.product-info > div.product-details > div > div.discount-percentage-enabled.discount-percentage-product-details.line-through.price-under-title > ul'))
        ) 
        # get the price from the page
        prices = self.driver.find_elements(By.CSS_SELECTOR, '#pip-river-container-WE > div.product-info-rvi > div.product-info > div.product-details > div > div.discount-percentage-enabled.discount-percentage-product-details.line-through.price-under-title > ul span.amount')
        # prices = price_container.find_elements(By.CSS_SELECTOR, 'span.amount')
        if (len(prices) == 0):
            return -1
        
        price = prices[len(prices) - 1].text
        return price

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, product_page_scraper, *args, **kwargs):
        self.product_page_scraper = product_page_scraper
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        url = params["url"][0]
        price = self.product_page_scraper.get_price(url)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        data = {'price': price}
        self.wfile.write(json.dumps(data).encode('utf-8'))


if __name__ == "__main__":
    driver = new_driver()
    product_page_scraper = ProductPageScraper(driver)
    handler = partial(MyServer, product_page_scraper)
    web_server = HTTPServer((hostName, serverPort), handler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")