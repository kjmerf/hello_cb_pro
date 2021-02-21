import argparse
import logging
import json
import os

from cbt import auth, private_client
from cbt.utils.clean_data import clean_candles
from cbt.utils.slack import post_to_channel

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", dest="action")
    args = parser.parse_args()

    host = os.getenv("PG_HOST")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    passphrase = os.getenv("CB_PASSPHRASE")
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")

    if args.action == "prepare":

        cb_auth = auth.get_cb_auth(api_key, api_secret, passphrase)
        pg_conn = auth.get_pg_conn(host, database, user, password)
        client = private_client.PrivateClient(cb_auth, pg_conn)
        client.create_database_objects()
        client.record_balances(dump="/tmp/accounts.json")
        client.load_candles()
        client.extract_candles(close_connection=True)
        clean_candles("/tmp/candles.csv", "/tmp/candles.json")

    elif args.action == "execute":

        cb_auth = auth.get_cb_auth(api_key, api_secret, passphrase)
        client = private_client.PrivateClient(cb_auth)

        with open("/tmp/decision.json") as f:
            data = json.load(f)
            decision = data["buy_or_sell"]
            amount = data["amount"]
            if decision == "buy":
                message = client.market_buy_btc(amount)
            elif decision == "sell":
                message = client.market_sell_btc(amount)
            else:
                raise ValueError(f"Expecting buy or sell but got {decision}!")

        if message:
            slack_message = [
                ":dog: Action taken in the market!",
                f"*Decision*: {decision}",
                f"*Amount*: {amount}",
                f"*Message*: {message}",
            ]
        else:
            slack_message = ":red_circle: Something went wrong! Better check the container logs."

        post_to_channel(slack_bot_token, slack_channel, "\n\t".join(slack_message))

    else:
        raise ValueError(f"Was expecting prepare or execute but got {args.action}")
