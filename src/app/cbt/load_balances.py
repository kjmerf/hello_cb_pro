import csv
from datetime import datetime, timezone
import logging
import os
import psycopg2

def load_balances(accounts):

    host = os.getenv("PG_HOST")
    database = os.getenv("PG_DATABASE")
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    port = int(os.getenv("PG_PORT", 25060))
    # slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    # slack_channel = os.getenv("SLACK_CHANNEL")

    now = datetime.now(timezone.utc)
    data_file_name = f"/tmp/accounts_{int(now.timestamp())}.csv"

    with open(data_file_name, "w") as f:
        writer = csv.writer(f, delimiter="|")
        for account in accounts:
            profile_id = account['profile_id']
            available = account['available']
            balance = account['balance']
            currency = account['currency']
            writer.writerow([profile_id] + [int(now.timestamp())] [available] + [balance] + [currency] + [int(now.timestamp())])

    conn = psycopg2.connect(
        host=host, database=database, user=user, password=password, port=port
    )

    logging.info("Creating database objects...")
    with open("/app/sql/create_objects.sql") as f:
        with conn:
            with conn.cursor() as curs:
                curs.execute(f.read())

    logging.info("Copying data to ODS...")
    with open(data_file_name) as f:
        with conn:
            with conn.cursor() as curs:
                curs.copy_from(f, "ods.balances", sep="|")

    conn.close()

    logging.info("Account balances successfully logged in database")

    """
    message = [
        ":white_check_mark: Data load complete!",
        f"*Product ID*: {product_id}",
        f"*Lookback*: {lookback} days",
        f"*Granularity*: {granularity} seconds",
        f"*Target table*: ods.candles",
    ]

    slack_response = requests.post(
        "https://slack.com/api/chat.postMessage",
        data={
            "token": slack_bot_token,
            "channel": slack_channel,
            "text": "\n\t".join(message),
            "as_user": True,
        },
    )
    logging.info(f"Status code from slack: {slack_response.status_code}")
    """