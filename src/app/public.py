from pprint import pprint
from datetime import datetime
from datetime import timedelta
import os

import requests

# https://docs.pro.coinbase.com/#get-historic-rates


def get_dates(lookback):

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=lookback)
    return start_date, end_date


if __name__ == "__main__":

    rest_url = os.getenv("CB_REST_URL")
    product_id = os.getenv("PRODUCT_ID")
    lookback = int(os.getenv("LOOKBACK"))
    granularity = os.getenv("GRANULARITY")

    start_date, end_date = get_dates(lookback)

    response = requests.get(
        f"{rest_url}/products/{product_id}/candles",
        params={
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "granularity": granularity,
        },
    )
    pprint(["time", "low", "high", "open", "close", "volume"])
    pprint(response.json())
