import logging
import os

from cbt import auth, private_client
from cbt.utils.slack import post_to_channel

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


if __name__ == "__main__":

    host = os.getenv("PG_HOST")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    cb_rest_url = os.getenv("CB_REST_URL", "https://api-public.sandbox.pro.coinbase.com")
    product_id = os.getenv("PRODUCT_ID", "BTC-USD")
    lookback = int(os.getenv("LOOKBACK", 1))
    granularity = int(os.getenv("GRANULARITY", 60))

    pg_conn = auth.get_pg_conn(host, database, user, password)
    client = private_client.PrivateClient(pg_conn=pg_conn, url_base=cb_rest_url)
    client.create_database_objects(False)
    client.load_candles(lookback, granularity, product_id, True)

    message = [
        ":white_check_mark: Data load complete!",
        f"*Product ID*: {product_id}",
        f"*Lookback*: {lookback} days",
        f"*Granularity*: 60 seconds",
        f"*Target table*: ods.candles",
    ]
    post_to_channel(slack_bot_token, slack_channel, "\n\t".join(message))
