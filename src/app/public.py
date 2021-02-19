from pprint import pprint
from datetime import datetime
from datetime import timedelta
import os

# we can ignore this import when unit testing
try:
    import requests
except ModuleNotFoundError:
    pass

# https://docs.pro.coinbase.com/#get-historic-rates


def yield_interval(last_time, lookback, granularity):
    """Yield interval

    Args:
        last_time (datetime.datetime): end of last interval
        lookback (int): number of days to lookback
        granularity (int): length of interval in seconds - must be 60, 300, 900, 3600, 21600 or 86400

    Yield:
        start and end of interval (both datetime.datetime objects)"""

    start_time = last_time - timedelta(days=lookback)
    t = start_time - timedelta(seconds=granularity)
    while t < last_time - timedelta(seconds=granularity):
        t += timedelta(seconds=granularity)
        yield t, t + timedelta(seconds=granularity)


def yield_batch(last_time, lookback, granularity, max_batch_size=300):
    """Yield batch

    Args:
        last_time (datetime.datetime): end of last interval
        lookback (int): number of days to lookback
        granularity (int): length of interval in seconds - must be 60, 300, 900, 3600, 21600 or 86400
        max_batch_size: max number of intervals in a single batch

    Yield:
        start and end of batch (both datetime.datetime objects)"""

    interval = 0
    for start_time, end_time in yield_interval(last_time, lookback, granularity):
        interval += 1
        if interval == 1:
            min_start_time = start_time
        if interval == max_batch_size or end_time == last_time:
            interval = 0
            yield min_start_time, end_time


if __name__ == "__main__":

    rest_url = os.getenv("CB_REST_URL")
    product_id = os.getenv("PRODUCT_ID")
    lookback = int(os.getenv("LOOKBACK"))
    granularity = int(os.getenv("GRANULARITY"))

    pprint(["time", "low", "high", "open", "close", "volume"])
    for start_time, end_time in yield_batch(
        datetime.utcnow(), lookback, granularity
    ):
        response = requests.get(
            f"{rest_url}/products/{product_id}/candles",
            params={
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "granularity": granularity,
            },
        )
        pprint(response.json())
