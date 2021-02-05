import base64
import hashlib
import hmac
import logging
import os
import requests
import time

from requests.auth import AuthBase

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    url = os.getenv("CB_URL")

    auth = CoinbaseExchangeAuth(api_key, api_secret, passphrase)
    logging.info("Making an authenticated call to the Coinbase Pro API...")
    accounts = requests.get(url + "/accounts", auth=auth).json()
    for account in accounts:
        balance = account["balance"]
        currency = account["currency"]
        logging.info(f"Your current {currency} balance is: {balance}.")

    logging.info("Making an unauthenticated call to the Coinbase Pro API...")
    currencies = requests.get(url + "/currencies").json()
    for currency in currencies:
        id = currency["id"]
        min_size = currency["min_size"]
        status = currency["status"]
        logging.info(f"{id} has a minimum size of {min_size} and a status of {status}.")
