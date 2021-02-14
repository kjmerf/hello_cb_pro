import argparse
from datetime import datetime
import json
import os
from time import sleep
import sys

import requests

import cbt.app.public as public

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback", dest="lookback", type=int)
    parser.add_argument("--granularity", dest="granularity", type=int)
    parser.add_argument("--product_id", dest="product_id")
    parser.add_argument("--output_file", dest="output_file")
    args = parser.parse_args()

    batch = 1
    with open(args.output_file, "w") as f:
        for start_time, end_time in public.yield_batch(
            datetime.utcnow(), args.lookback, args.granularity
        ):
            print(f"Getting data for interval {start_time} to {end_time}...")
            response = requests.get(
                f"https://api-public.sandbox.pro.coinbase.com/products/{args.product_id}/candles",
                params={
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "granularity": args.granularity,
                },
            )
            data = response.json()
            data.sort()
            for rate in data:
                d = {}
                d["time"] = rate[0]
                d["low"] = rate[1]
                d["high"] = rate[2]
                d["open"] = rate[3]
                d["close"] = rate[4]
                d["volume"] = rate[5]
                d["iso_time"] = datetime.fromtimestamp(rate[0]).isoformat()
                d["batch"] = batch
                json.dump(d, f)
                f.write("\n")
            batch += 1
            # sleeping to avoid hitting the rate limit
            sleep(0.1)

    print(f"Wrote {args.lookback} days of data to {args.output_file}!")
