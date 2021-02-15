import argparse
from datetime import datetime
import json
import os
from time import sleep
import sys

import requests

sys.path.append(f"{os.getcwd()}/src/app")
import private

from cbt.wrappers import market_buy_btc


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--usd", dest="usd", type=float)
    args = parser.parse_args()

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")

    auth = private.CoinbaseExchangeAuth(api_key, api_secret, passphrase)
    market_buy_btc(auth, args.usd)
