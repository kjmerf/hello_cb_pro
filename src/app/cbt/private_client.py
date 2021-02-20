import os
import requests
import uuid

from cbt.cb_api import market_order_btc, get_accounts
from cbt.load_balances import load_balances

class PrivateClient:
    def __init__(self, auth, url_base=os.getenv("CB_REST_URL")):
        self.url_base = url_base
        self.auth = auth
        self.latest_uuid = str(uuid.uuid4())

    def get_accounts(self):
        return requests.get(f"{self.url_base}/accounts", auth=self.auth)

    def record_balances(self):
        accounts = get_accounts(self.auth)
        load_balances(accounts)

    def market_buy_btc(self, usd):
        market_order_btc("buy", self.auth, usd, self.latest_uuid)
        self.update_uuid()

    def market_sell_btc(self, usd):
        market_order_btc("sell", self.auth, usd, self.latest_uuid)
        self.update_uuid()

    def update_uuid(self):
        self.latest_uuid == str(uuid.uuid4())
