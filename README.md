# hello_cb_pro

This purpose of this repo is to explore the Coinbase Pro Sandbox API.
The Sandbox API mimics the production one.
Before getting started check out: https://docs.pro.coinbase.com.

# Overview

There are six services that can be run.
Three of them simply get and print data: private, public, and ws (websocket).
The private service makes an authenticated call to the Sandbox API to retreive account information.
The public service makes an unathenticated call to the Sandbox API to get historical price data.
The ws service makes an unathenticated connection to the Sandbox Websocket to subscribe to real-time market data.
If you're new to the project, it's worth checking these out before moving on to the others.

The other services allow you to buy and sell BTC, and load data to the project database.
See below for more details.

## Setup

To use the private service, you first need to create an account here: https://public.sandbox.pro.coinbase.com. If you have a real Coinbase account, it should automatically link to that, but none of your real assets will be loaded.
Then create an API key associated with the account and set the following environment variables accordingly:
```CB_API_KEY```, ```CB_API_SECRET``` and ```CB_PASSPHRASE```.

## Running services locally

```shell
# build and run the private service
docker-compose up --build --remove-orphans private

# build and run the public service
docker-compose up --build --remove-orphans public

# build and run the ws service
docker-compose up --build --remove-orphans ws
```

## Getting data

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

## Buying and selling (fake) BTC

To see if you can translate your fake USD to fake BTC from the command line, try the `buy_btc` service
```shell
# note the syntax
USD_BUY=1000 docker-compose up --build --remove-orphans buy_btc
USD_SELL=100 docker-compose up --build --remove-orphans sell_btc
```

## Loading data

We created a postgres database for the project.
To load data into the database, you need to setup the following environment variables:
```PG_HOST```, ```PG_DATABASE```, ```PG_USER```, ```PG_PASSWORD```, ```SLACK_BOT_TOKEN```, and ```SLACK_CHANNEL```.
Then you can run:
```shell
docker-compose up --build --remove-orphans load_candles
````

## Unit testing

We only have a couple tests at this point.
You can run them with ```make test```.
