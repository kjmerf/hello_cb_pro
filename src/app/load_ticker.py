from json import dumps
from pprint import pprint
import os

import websocket

from cbt import auth, private_client

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
                "name": os.getenv("CHANNEL", "ticker"),
                "product_ids": [os.getenv("PRODUCT_ID", "BTC-USD")],
            }
        ],
    }
    ws.send(dumps(params))


if __name__ == "__main__":

    host = os.getenv("PG_HOST")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")

    pg_conn = auth.get_pg_conn(host, database, user, password)
    client = private_client.PrivateClient(pg_conn=pg_conn)
    client.create_database_objects(True)

    # websocket.enableTrace(True)
    # ws = websocket.WebSocketApp(
    #     "wss://ws-feed.pro.coinbase.com", on_message=on_message, on_error=on_error, on_close=on_close,
    # )
    # ws.on_open = on_open
    # ws.run_forever()
