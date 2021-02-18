#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:11:51 2021

@author: steve
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import seaborn as sns

import statsmodels.api as sm

## Standard Functions
def calc_performance(returns, freq):
    
    assert isinstance(returns, pd.DataFrame) # data type check
    
    """ Calculate performance statistics
    Parameters:
    df (dataframe): dataframe of returns specified by the frequency
    freq (int): 4 for qtrly, 12 for monthly, 252 for daily
    """
    names = returns.columns
    stats = pd.DataFrame(columns = names,
                         index=['Daily Returns', 'Daily Vol', 'Sharpe',
                                'Downside Vol', 'Sortino'])
    stats.iloc[0, :] = np.round((returns.mean().values * freq * 100), 2)
    stats.iloc[1, :] = np.round((returns.std().values * np.sqrt(freq) * 100), 2)
    stats.iloc[2, :] = stats.iloc[0, :] / stats.iloc[1, :]
    stats.iloc[3, :] = np.round((returns.apply(lambda col:
                                     np.std(col[col < 0])).values * \
                                     np.sqrt(freq) * 100), 2)
    stats.iloc[4, :] = stats.iloc[0, :] / stats.iloc[3, :]
    return stats

def getTvalue(prices):
    # get t-value from a linear model
    x = np.ones((prices.shape[0],2))
    x[:, 1] = np.arange(prices.shape[0])
    ols = sm.OLS(prices, x).fit()
    return ols.tvalues[1]

def getTrendLabels(dates, close, span):
    '''
    Derive labels from the sign of t-value of linear trend
    Output:
        t1: end time for the identified trend
        tVal: t-value associated with the estimated trend coefficient
        sign: sign of the trend
    '''
    out = pd.DataFrame(index=dates, columns=['t1', 'tVal', 'sign'])
    hrzns = range(*span)
    
    for dt0 in dates:
        df0 = pd.Series()
        iloc0 = close.index.get_loc(dt0)
        if iloc0 + max(hrzns) > close.shape[0]: continue
        for hrzn in hrzns:
            dt1 = close.index[iloc0 + hrzn - 1]
            df1 = close.loc[dt0:dt1]
            df0.loc[dt1] = getTvalue(df1.values)
        dt1 = df0.replace([-np.inf, np.inf, np.nan], 0).abs().idxmax()
        out.loc[dt0,['t1','tVal','sign']] = df0.index[-1], df0[dt1], np.sign(df0[dt1])
    
    out['t1'] = pd.to_datetime(out['t1'])
    out['sign'] = pd.to_numeric(out['sign'], downcast = 'signed')
    
    return out.dropna(subset=['sign']) 

def getBestTrend(dates, close, lookback):
    '''
    Derive labels from the sign of t-value of linear trend
    Output:
        t1: end time for the identified trend
        tVal: t-value associated with the estimated trend coefficient
        sign: sign of the trend
    '''
    out = pd.DataFrame(index=dates, columns=['t0', 'tVal', 'sign'])
    hrzns = range(*lookback)
    dts = dates[max(hrzns):]
    
    for dt1 in dts:
        df0 = pd.Series()
        iloc1 = close.index.get_loc(dt1)
        if iloc1 > close.shape[0]: continue
        for hrzn in hrzns:
            dt0 = close.index[iloc1 - hrzn]
            df1 = close.loc[dt0:dt1]
            df0.loc[dt0] = getTvalue(df1.values)
        best_dt = df0.replace([-np.inf, np.inf, np.nan], 0).abs().idxmax()
        out.loc[dt1,['t0','tVal','sign']] = best_dt, df0[best_dt], np.sign(df0[best_dt])
    
    out['t0'] = pd.to_datetime(out['t0'])
    out['sign'] = pd.to_numeric(out['sign'], downcast = 'signed')
    
    return out.dropna(subset=['sign'])    

def getMeanTrend(dates, close, lookback):
    '''
    Derive labels from the sign of t-value of linear trend
    Output:
        tVal: t-value associated with the estimated trend coefficient
        sign: sign of the trend
    '''
    out = pd.DataFrame(index=dates, columns=['tVal', 'sign'])
    hrzns = lookback
    dts = dates[max(hrzns):]
    signal = 0
    for dt1 in dts:
        df0 = pd.Series(dtype = 'float64')
        iloc1 = close.index.get_loc(dt1)
        if iloc1 > close.shape[0]: continue
        for hrzn in hrzns:
            dt0 = close.index[iloc1 - hrzn]
            df1 = close.loc[dt0:dt1]
            df0.loc[dt0] = getTvalue(df1.values)
        mean_trend = df0.mean()
        if mean_trend > 0 and mean_trend < 10: 
            signal = 1
        elif mean_trend >= 10: 
            signal = 0
        elif mean_trend <-2 and mean_trend > -8:
            signal = 0
        elif mean_trend <= -8: # BTFD
            signal = 1 
#        elif signal == 1 and mean_trend < 0:
#            signal = 1
        else: 
            signal = 1
        out.loc[dt1,['tVal','sign']] = mean_trend, signal
    
    out['sign'] = pd.to_numeric(out['sign'], downcast = 'signed')
    
    return out.dropna(subset=['sign'])                        
            

## Load data 
df = pd.read_csv('data/bitcoin.csv')
close = df['close']
close = close[close.between(close.quantile(.02), 
                                     close.quantile(.98))]
close_df = close.to_frame()
time_df = df['iso_time'].to_frame()
time_df = time_df.drop_duplicates()

close_df = close_df.merge(time_df, left_index=True, right_index=True)

close_df.set_index('iso_time', inplace=True)
close_df.index = pd.to_datetime(close_df.index)

# 1-period forward returns
fwd_1p = (close_df.shift(-1)/ close_df - 1)
fwd_1p_clean = fwd_1p[fwd_1p['close'].between(fwd_1p['close'].quantile(.02), 
                                     fwd_1p['close'].quantile(.98))]
fwd_1p_clean = fwd_1p.merge(fwd_1p_clean, left_index=True, right_index=True, how='outer')
fwd_1p_clean.fillna(0.0, inplace=True)
fwd_1p_clean.drop(['close_x'], axis=1, inplace=True)
fwd_1p_clean.columns = ['btc']


# get average historical trend and generate labels
df1 = getMeanTrend(close_df.index, close_df, [5, 20, 50, 100, 200])

df_merged = pd.merge(df1, fwd_1p_clean, how='left', left_index=True, right_index=True)
df_merged['model'] = df_merged['sign']*df_merged['btc']
out = df_merged.loc[:,['btc','model', 'tVal', 'sign']]
stats = out.describe()
print(stats)

merged_returns = df_merged.loc[:,['btc','model']]

# inputs: returns df and frequency scalar
perf = calc_performance(merged_returns, 24) # 24 hours in a day
print(perf)

model_tr = pd.Series(np.cumprod(1 + out['model'].values), 
                                   index=out.index).rename('model')

bench_tr = pd.Series(np.cumprod(1 + out['btc'].values), 
                                   index=out.index).rename('naive')

plt.plot(model_tr.index, model_tr, label='model')
plt.plot(bench_tr.index, bench_tr, label='naive')
plt.ylabel('Cumulative % Returns')
plt.axis('tight')
plt.legend()
plt.title('Trend-following model vs. naive benchmark')
plt.show()

