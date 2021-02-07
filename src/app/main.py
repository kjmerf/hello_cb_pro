from json import dumps
from time import sleep
import logging
import os

import requests
import websocket

import authentication

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def on_message(ws, message):
    logging.info(message)


def on_error(ws, error):
    logging.warning(error)


def on_close(ws):
    logging.info("### closed ###")


def on_open(ws):
    params = {
        "type": "subscribe",
        "channels": [
            {
                "name": os.getenv("CHANNEL"),
                "product_ids": [os.getenv("PRODUCT_ID")],
            }
        ],
    }
    ws.send(dumps(params))


if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    rest_url = os.getenv("CB_REST_URL")
    websocket_url = os.getenv("CB_WEBSOCKET_URL")

    auth = authentication.CoinbaseExchangeAuth(api_key, api_secret, passphrase)
    logging.info("Making an authenticated call to the Coinbase Pro REST API...")
    accounts = requests.get(rest_url + "/accounts", auth=auth).json()
    for account in accounts:
        balance = account["balance"]
        currency = account["currency"]
        logging.info(f"Your current {currency} balance is: {balance}.")

    # just to give you time to read the account balances
    sleep(5)
    logging.info("Making an unathenticated connection to the Coinbase Pro Websocket...")
    sleep(5)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
