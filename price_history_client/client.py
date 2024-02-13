# import packages
import argparse
import requests


def main():
    # read flags to get the url of the server
    parser = argparse.ArgumentParser()
    parser.add_argument("--web_url", type=str, required=True)
    parser.add_argument("--scraper_url", type=str, required=True)
    args = parser.parse_args()
    web_url = args.web_url
    scraper_url = args.scraper_url

    # make a request to web server to retrieve a list of price watchers
    response = requests.get(web_url + "/watchers")
    watchers = response.json()

    # for each watcher, make a request to the scraper server to get the price
    for watcher in watchers:
        response = requests.get(scraper_url + "/get_price?url=" + watcher.url)
        price = response.json()["price"]
        
        # make a request to the web server to update the price
        requests.post(web_url + "/update_price", json={"url": watcher.url, "price": price})


