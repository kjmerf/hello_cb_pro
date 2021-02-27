# hello_cb_pro

This purpose of this repo is to explore the Coinbase Pro Sandbox API. 

# Overview

This repo contains several (docker) services that can be used to interact with the Coinbase Pro Sandbox API.
The repo also contains ad hoc scripts that can be used to pull data and perform analysis.

## Setup

Before getting started, you'll need to create an account here: https://public.sandbox.pro.coinbase.com.
If you have a real Coinbase account, it should automatically link to that, but none of your real assets will be loaded.
Then create an API key associated with the account and set the following environment variables accordingly:
```CB_API_KEY```, ```CB_API_SECRET``` and ```CB_PASSPHRASE```.

## Buying and selling crypto

If you want to buy and sell crypto, you can use the ```buy_btc``` and ```sell_btc``` services.
You don't need database or slack credentials setup to run these services but you do need to your Coinbase Pro credentials setup as described above.
To run the service simply run:

```shell
USD_BUY=1000 docker-compose up --build --remove-orphans buy_btc
BTC_SELL=.001 docker-compose up --build --remove-orphans sell_btc
```

You should be able to validate that the transactions went through my checking the UI: https://public.sandbox.pro.coinbase.com.

## Loading historical data to the database

To (batch) load historical data to the database, you can use the ```load_candles``` service:

```shell
docker-compose up --build --remove-orphans load_candles
```

## Streaming data to the database

To stream real-time data to the database, you can use the ```load_ticker``` service.

```shell
docker-compose up --build --remove-orphans load_ticker
```

## Getting data from the REST API

If you want to download historical data into a local file, you can use the ```get_data.py``` script.

```shell
# install the requirements in a virtual environment
pip install -r scripts/requirements.txt
# run the script
python scripts/get_data.py --lookback 200 --granularity 3600 --product_id BTC-USD --output_file /tmp/cb_pro.json
```

With those arguments, you'll get 200 days worth of data at the hourly level, for the BTC-USD product.
The data will be written to ```tmp/cb_pro.json```.
You can adjust the arguments as needed.

The data will be written as newline delimited JSON.
To read the file into a dataframe, you can use:
```python
import pandas as pd
df = pd.read_json("/tmp/cb_pro.json", lines=True)
```

## Getting data from the Websocket

If you want to print real-time data from the websocket, you use use the ```ws.py``` script.

```shell
# install the requirements in a virtual environment
pip install -r scripts/requirements.txt
# run the script
python scripts/ws.py
```

## Unit testing

We only have a couple tests at this point.
You can run them with ```make test```.
