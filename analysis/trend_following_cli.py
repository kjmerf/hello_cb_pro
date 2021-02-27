#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:11:51 2021

@author: steve
"""
import sys
import json

import numpy as np
import pandas as pd
import statsmodels.api as sm


def getTvalue(prices):
    # get t-value from a linear model
    x = np.ones((prices.shape[0], 2))
    x[:, 1] = np.arange(prices.shape[0])
    ols = sm.OLS(prices, x).fit()
    return ols.tvalues[1]


def getMeanTrend(dates, close, lookback):
    """
    Derive labels from the sign of t-value of linear trend
    Output:
        tVal: t-value associated with the estimated trend coefficient
        sign: sign of the trend
    """
    if close.shape[0] < 201:
        raise ValueError("Need at least 201 hours of data")
    out = pd.DataFrame(index=dates, columns=["tVal", "sign"])
    hrzns = lookback
    dts = dates[max(hrzns) :]
    signal = 0
    for dt1 in dts:
        df0 = pd.Series(dtype="float64")
        iloc1 = close.index.get_loc(dt1)
        if iloc1 > close.shape[0]:
            continue
        for hrzn in hrzns:
            dt0 = close.index[iloc1 - hrzn]
            df1 = close.loc[dt0:dt1]
            df0.loc[dt0] = getTvalue(df1.values)
        mean_trend = df0.mean()
        if mean_trend >= 0 and mean_trend < 12:  # TREND IS YOUR FRIEND
            signal = 1
        elif mean_trend < 0 and mean_trend > -10:  # GTFO
            signal = 0
        elif mean_trend <= -10:  # BTFDeepDIP
            signal = 1

        else:
            signal = 1
        out.loc[dt1, ["tVal", "sign"]] = mean_trend, signal

    out["sign"] = pd.to_numeric(out["sign"], downcast="signed")

    return out.dropna(subset=["sign"])


def main(args):

    # python trend_following_cli.py path-to-input-file path-to-account-info
    """ args:
        path-to-input-file: csv containing last 201 hours of close data
        path-to-account-info: json of btc and usd account information
    """
    df = pd.read_json(args[1], lines=True)
    acct = json.load(open(args[2]))
    # TODO: data cleaning function
    close = df["close"]
    close = close[close.between(close.quantile(0.02), close.quantile(0.98))]
    close_df = close.to_frame()
    time_df = df["iso_time"].to_frame()
    time_df = time_df.drop_duplicates()
    close_df = close_df.merge(time_df, left_index=True, right_index=True)
    close_df.set_index("iso_time", inplace=True)
    close_df.index = pd.to_datetime(close_df.index)

    # getMeanTrend which will return a signal (long = 1, flat = 0)
    close_df = close_df.tail(201)
    signal = getMeanTrend(close_df.index, close_df, [5, 20, 50, 100, 200])

    # Compare the signal to current portfolio
    # Get USD and BTC balances
    usd = [np.float(a["balance"]) for a in acct if a["currency"] == "USD"][0]
    btc = [np.float(a["balance"]) for a in acct if a["currency"] == "BTC"][0]
    order = {}
    if signal["sign"][0] == 1:
        if usd > 0:
            order = {"order_type": "market", "buy_or_sell": "buy", "amount": usd}
    elif signal["sign"][0] == 0:
        if btc > 0:
            order = {"order_type": "market", "buy_or_sell": "sell", "amount": btc}

    return print(json.dumps(order))


if __name__ == "__main__":

    main(sys.argv)
