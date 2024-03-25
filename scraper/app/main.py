import argparse
import logging
import json
import requests
from decimal import *
from functools import partial
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  
import undetected_chromedriver as uc

hostName = "0.0.0.0"
serverPort = 8081

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
            return {"error": "invalid url", price: 0}
         
        # navigate to the URL
        self.driver.get(url)

        # Check if request was blocked
        if '403' in self.driver.title:
            return {"error": "request blocked", price: 0}
        
        # wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pip-river-container-WE > div.product-info-rvi > div.product-info > div.product-details > div > div.discount-percentage-enabled.discount-percentage-product-details.line-through.price-under-title > ul'))
        ) 
        # get the price from the page
        prices = self.driver.find_elements(By.CSS_SELECTOR, '#pip-river-container-WE > div.product-info-rvi > div.product-info > div.product-details > div > div.discount-percentage-enabled.discount-percentage-product-details.line-through.price-under-title > ul span.amount')
        # prices = price_container.find_elements(By.CSS_SELECTOR, 'span.amount')
        if (len(prices) == 0):
            return {"error": "couldn't parse price", price: 0}
        
        price = prices[len(prices) - 1].text
        return {"price": Decimal(price.replace(",", "")), "error": None}


def main():
    logging.basicConfig(level=logging.INFO)
    driver = new_driver()
    product_page_scraper = ProductPageScraper(driver)
    # read flags to get the url of the server
    parser = argparse.ArgumentParser()
    parser.add_argument("--web_url", type=str, required=False, default="http://price-tracker-nlb-69684cb79f3a9e04.elb.us-east-2.amazonaws.com")
    args = parser.parse_args()
    web_url = args.web_url

    # make a request to web server to retrieve a list of price watchers
    response = requests.get(web_url + "/api/watchers/")
    watchers = response.json()

    # for each watcher, make a request to the scraper server to get the price
    for watcher in watchers:
        price = product_page_scraper.get_price(watcher['url'])
        if price["error"] is not None:
            logging.error(f"Error getting price for {watcher['url']}: {price['error']}")
            continue
        
        logging.info(f"Price for {watcher['url']} is {price}")
        # make a request to the web server to update the price
        r = requests.post(web_url + "/api/prices/", json={"watcher_id": watcher['id'], "price": price})
        if r.status_code != 200:
            logging.error(f"Error updating price for {watcher['url']}: status: {r.status_code}, message: {r.text}")
            continue

        logging.info(f"Successfully updated price for {watcher['url']}")    


    # close the driver
    driver.close()

if __name__ == "__main__":
    main()


