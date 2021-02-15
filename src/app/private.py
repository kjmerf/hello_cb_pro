from pprint import pprint
import base64
import hashlib
import hmac
import os
import time

from requests.auth import AuthBase
import requests

# https://docs.pro.coinbase.com/#private


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = "".join(
            [timestamp, request.method, request.path_url, (request.body or b"")]
        )
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update(
            {
                "CB-ACCESS-SIGN": signature_b64,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-ACCESS-KEY": self.api_key,
                "CB-ACCESS-PASSPHRASE": self.passphrase,
                "Content-Type": "application/json",
            }
        )
        return request


if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    rest_url = os.getenv("CB_REST_URL")
    request_suffix = os.getenv("REQUEST_SUFFIX")

    auth = CoinbaseExchangeAuth(api_key, api_secret, passphrase)
    accounts = requests.get(f"{rest_url}/{request_suffix}", auth=auth)
    pprint(accounts.json())
