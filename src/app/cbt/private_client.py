import json
import requests
import uuid

from cbt.cb_api import market_order_btc, get_accounts
from cbt.pg import load_balances, load_candles, create_database_objects, extract_candles


class PrivateClient:
    """Client that can be used for interacting with the Coinbase exchange as well as our Postgres instance"""

    def __init__(
        self, cb_auth, pg_conn=None, url_base="https://api-public.sandbox.pro.coinbase.com"
    ):
        """Constructor

        Args:
            cb_auth: CoinbaseExchangeAuth object
            pg_conn: psycopg2.extensions.connection object
            url_base: Coinbase exchange URL

        Output:
            None"""

        self.url_base = url_base
        self.cb_auth = cb_auth
        self.latest_uuid = str(uuid.uuid4())
        self.pg_conn = pg_conn

    def get_accounts(self):
        return requests.get(f"{self.url_base}/accounts", cb_auth=self.cb_auth)

    def record_balances(self, dump=None, close_connection=False):
        accounts = get_accounts(self.url_base, self.cb_auth)
        load_balances(accounts, self.pg_conn, close_connection)

        if dump:
            with open(dump, "w") as f:
                json.dump(accounts, f)

    def market_buy_btc(self, usd):
        message = market_order_btc(self.url_base, "buy", self.cb_auth, usd, self.latest_uuid)
        self.update_uuid()
        return message

    def market_sell_btc(self, btc):
        message = market_order_btc(self.url_base, "sell", self.cb_auth, btc, self.latest_uuid)
        self.update_uuid()
        return message

    def update_uuid(self):
        self.latest_uuid == str(uuid.uuid4())

    def load_candles(self, close_connection=False):
        load_candles(self.url_base, self.pg_conn, close_connection=close_connection)

    def create_database_objects(self, close_connection=False):
        create_database_objects(self.pg_conn, close_connection)

    def extract_candles(self, close_connection=False):
        extract_candles(self.pg_conn, close_connection)
