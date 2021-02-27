import logging
import os

from cbt.private_client import PrivateClient
from cbt.auth import get_cb_auth

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    btc = os.getenv("BTC_SELL", "0.001")

    auth = get_cb_auth(api_key, api_secret, passphrase)
    client = PrivateClient(cb_auth=auth)
    client.market_sell_btc(btc)
