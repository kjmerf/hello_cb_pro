from datetime import datetime, timezone
from json import dumps, loads
import logging
from pprint import pprint
import os

import websocket

from cbt import auth, private_client

# https://docs.pro.coinbase.com/#websocket-feed

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def on_message(ws, message):

    host = os.getenv("PG_HOST")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")

    data = loads(message)
    if "price" in data:
        pg_conn = auth.get_pg_conn(host, database, user, password)
        with pg_conn:
            with pg_conn.cursor() as curs:
                curs.execute(
                    "INSERT INTO landing.ticker (type, trade_id, sequence, time, product_id, price, side, last_size, best_bid, best_ask, created_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  # noqa
                    (
                        data["type"],
                        data["trade_id"],
                        data["sequence"],
                        data["time"],
                        data["product_id"],
                        data["price"],
                        data["side"],
                        data["last_size"],
                        data["best_bid"],
                        data["best_ask"],
                        datetime.now(timezone.utc).isoformat()
                    ),
                )

        pg_conn.close()
        logging.info(f"Inserted {message} into landing.ticker!")


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
    client.create_database_objects()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://ws-feed.pro.coinbase.com", on_message=on_message, on_error=on_error, on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
