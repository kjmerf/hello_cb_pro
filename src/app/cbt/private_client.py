import os
import requests

from cbt.cb_api import market_buy_btc
from cbt.cb_api import market_sell_btc


class PrivateClient:
    def __init__(self, auth, url_base=os.getenv("CB_REST_URL")):
        self.url_base = url_base
        self.auth = auth

    def get_accounts(self):
        return requests.get(f"{self.url_base}/accounts", auth=self.auth)

    def market_buy_btc(self, usd):
        return market_buy_btc(self.auth, usd)

    def market_sell_btc(self, usd):
        return market_sell_btc(self.auth, usd)
