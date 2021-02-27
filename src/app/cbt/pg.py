import csv
from datetime import datetime, timezone
import logging
from time import sleep

import requests

from cbt.utils.date_utils import yield_batch

# leaving contexts doesn't close the connection
# https://www.psycopg.org/docs/connection.html


def create_database_objects(conn, close_connection=True):
    logging.info("Creating database objects...")
    with open("/app/sql/create_objects.sql") as f:
        with conn:
            with conn.cursor() as curs:
                curs.execute(f.read())

    logging.info("Database objects created!")

    if close_connection:
        logging.info("Closing database connection...")
        conn.close()


def load_balances(accounts, conn, close_connection=True):

    now = datetime.now(timezone.utc)
    data_file_name = f"/tmp/balances_{int(now.timestamp())}.csv"

    with open(data_file_name, "w") as f:
        writer = csv.writer(f, delimiter="|")
        for account in accounts:
            profile_id = account["profile_id"]
            available = account["available"]
            balance = account["balance"]
            currency = account["currency"]
            writer.writerow(
                [profile_id]
                + [available]
                + [balance]
                + [currency]
                + [int(now.timestamp())]
            )

    logging.info("Copying data to ods.balances...")
    with open(data_file_name) as f:
        with conn:
            with conn.cursor() as curs:
                curs.copy_from(f, "ods.balances", sep="|")

    logging.info("Account balances successfully written to database!")

    if close_connection:
        logging.info("Closing database connection...")
        conn.close()


def load_transaction(transaction, conn, close_connection=True):

    now = datetime.now(timezone.utc)
    data_file_name = f"/tmp/transaction_{int(now.timestamp())}.csv"

    with open(data_file_name, "w") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(transaction.to_pg_row() + [int(now.timestamp())])

    logging.info("Copying data to ods.transactions...")
    with open(data_file_name) as f:
        with conn:
            with conn.cursor() as curs:
                curs.copy_from(f, "ods.transactions", sep="|")

    logging.info("Transaction successfully written to database!")

    if close_connection:
        logging.info("Closing database connection...")
        conn.close()


def load_candles(
    url, conn, lookback=1, granularity=60, product_id="BTC-USD", close_connection=True
):

    now = datetime.now(timezone.utc)
    data_file_name = f"/tmp/candles_{int(now.timestamp())}.csv"
    with open(data_file_name, "w") as f:
        writer = csv.writer(f, delimiter="|")
        for start_time, end_time in yield_batch(now, lookback, granularity):
            logging.info(f"Getting data for interval {start_time} to {end_time}...")
            response = requests.get(
                f"{url}/products/{product_id}/candles",
                params={
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "granularity": granularity,
                },
            )
            data = response.json()
            for row in data:
                writer.writerow([product_id] + row + [int(now.timestamp())])

            # sleeping to avoid hitting the rate limit
            sleep(0.2)

    logging.info("Copying data to landing.candles...")
    with open(data_file_name) as f:
        with conn:
            with conn.cursor() as curs:
                curs.copy_from(f, "landing.candles", sep="|")

    logging.info("Loading ods.candles...")
    with open("/app/sql/load_ods_candles.sql") as f:
        with conn:
            with conn.cursor() as curs:
                curs.execute(f.read())

    logging.info("Candles successfully written to database!")

    if close_connection:
        logging.info("Closing database connection...")
        conn.close()


def extract_candles(
    conn, close_connection=True
):
    logging.info("Extracting candles to local file...")
    with open("/tmp/candles.csv", "w") as f:
        with conn:
            with conn.cursor() as curs:
                curs.copy_to(f, "ods.candles", sep="|")

    logging.info("Candles successfully extracted from database!")

    if close_connection:
        logging.info("Closing database connection...")
        conn.close()
