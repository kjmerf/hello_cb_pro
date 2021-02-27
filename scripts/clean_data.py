from datetime import datetime
import logging

import pandas as pd


def clean_candles(input_file, output_file, product_id="BTC-USD"):
    """Clean the candles extract

    Args:
        product_id: filter the extract on this product ID

    Output:
        None"""

    logging.info("Cleaning candles data...")

    with open(output_file, "w") as f:

        for chunk in pd.read_csv(
            input_file,
            sep="|",
            chunksize=1000,
            names=[
                "product_id",
                "time",
                "low",
                "high",
                "open",
                "close",
                "volume",
                "created_time",
            ],
        ):
            chunk["product_id"] = chunk["product_id"].str.strip()
            chunk = chunk[chunk["product_id"] == product_id]
            chunk["iso_time"] = chunk["time"].apply(lambda x: datetime.fromtimestamp(x).isoformat())
            if not chunk.empty:
                chunk.to_json(f, orient="records", lines=True)
