#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:43:38 2021

@author: steve
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.stats.stats import pearsonr 

df = pd.read_json("/tmp/cb_pro.json", lines=True)
df.to_csv('data/bitcoin.csv', index=False)

df = pd.read_csv('data/bitcoin.csv')
close = df['close']
close = close[close.between(close.quantile(.02), 
                                     close.quantile(.98))]

# Correlation tests
periods = [10, 20, 30, 50, 75, 100]

returns_lagged = {}
returns_fwd = {}
for p in periods:
    lagged = close.pct_change(p)
    returns_lagged[p] = lagged.fillna(0.0003)
    fwd = close.pct_change(p).shift(-p)
    returns_fwd[p] = fwd.fillna(0.0003)

correl_tests = {}
    
for l in periods:
    for f in periods:
        correl_tests[l,f] = pearsonr(returns_lagged[l].values, returns_fwd[f].values)[0]
# the strongest correlation was between a 10-hour lookback and 
# 10-hour holding period. This is cheating but we will test it anyway.

# Quick bactest

lookback = 10
hold_period = 10

longs = close < close.shift(lookback)
shorts = close > close.shift(lookback)
dret = []

if close < close.shift(lookback):




        
    
        


    
