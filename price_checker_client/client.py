import argparse
import requests
import smtplib

def main():
    # read flags to get the url of the server
    parser = argparse.ArgumentParser()
    parser.add_argument("--web_url", type=str, required=True, default="http://localhost/app")
    parser.add_argument("--smtp_server_address", type=str, required=True)
    parser.add_argument("--smtp_server_port", type=int, required=True)
    parser.add_argument("--smtp_username", type=str, required=True)
    parser.add_argument("--smtp_password", type=str, required=True)
    parser.add_argument("--smtp_from_email", type=str, required=True)
    parser.add_argument("--smtp_to_email", type=str, required=True)
    args = parser.parse_args()
    web_url = args.web_url
    smtp_server_address = args.smtp_server_address
    smtp_server_port = args.smtp_server_port
    smtp_username = args.smtp_username
    smtp_password = args.smtp_password
    from_email = args.smtp_from_email
    to_email = args.smtp_to_email

    # make a request to web server to retrieve a list of URLs of product pages
    response = requests.get(web_url + "/watchers")
    watchers = response.json()

    notify_products = []
    # for each watcher, make a request to the scraper server to get the price
    for watcher in watchers:
        response = requests.get(web_url + "/price_history?url=" + watcher.url)
        price_history = response.json()["price"]
        
        # check if the price has dropped more than 20%
        if price_history[0].price > price_history[1].price * 0.8:
            # add to the list of products to notify of the drop in price
            notify_products.append({"product": watcher, "price_drop": price_history[0].price - price_history[1].price, "price_drop_percentage": (price_history[0].price - price_history[1].price) / price_history[1].price * 100})
        else:
            print("Price has not dropped enough to notify the user")
    
    # make a request to the web server to retrieve a list of recently sent notifications
    response = requests.get(web_url + "/notifications?duration=1month")
    recent_notifications = response.json()

    # filter out products for which a notification was sent in the last month
    notify_products = [product for product in notify_products if not product.product.url in map(lambda recent_notification: recent_notification.url, recent_notifications)]

    if len(notify_products) == 0:
        print("No products to notify")
        return

    # send an email to the user for each product in the list of products to notify
    subject = 'Price drops!'
    # format each price drop notification as a list item
    body = '''
    <ul>
        {0}
    </ul>
    '''.format(''.join([f'<li>{product.product.url} has dropped by {product.price_drop} ({product.price_drop_percentage}%)</li>' for product in notify_products]))

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(smtp_server_address, smtp_server_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(from_email, to_email, message)