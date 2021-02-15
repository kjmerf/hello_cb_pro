from json import dumps
from pprint import pprint
import os

import websocket

# https://docs.pro.coinbase.com/#websocket-feed


def on_message(ws, message):
    pprint(message)


def on_error(ws, error):
    pprint(error)


def on_close(ws):
    pprint("### closed ###")


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

    websocket_url = os.getenv("CB_WEBSOCKET_URL")

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
