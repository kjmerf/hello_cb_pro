# hello_cb_pro

This purpose of this repo is to explore the Coinbase Pro Sandbox API.
The Sandbox API mimics the production one.
Before getting started check out: https://docs.pro.coinbase.com.

# Overview

There are there services that can be run: private, public, and ws (websocket).
The private service makes an authenticated call to the Sandbox API to retreive account information.
The public service makes an unathenticated call to the Sandbox API to get historical price data.
The ws service makes an unathenticated connection to the Sandbox Websocket to subscribe to real-time market data.

## Setup

To use the private service, you first need to create an account here: https://public.sandbox.pro.coinbase.com.
Then create an API key associated with the account and set the following environment variables accordingly:
```CB_API_KEY```, ```CB_API_SECRET``` and ```CB_PASSPHRASE```.

## Running services locally

```shell
# build and run the private service
docker-compose build private
docker-compose run private

# build and run the public service
docker-compose build public
docker-compose run public

# build and run the ws service
docker-compose build ws
docker-compose run ws
```

## Getting data

If you want to download historical rates into a local file, you can use the ```get_data.py``` script.

```shell
# install the requirements in a virtual environment
pip install -r scripts/get_data_requirements.txt
# run the script
python scripts/get_data.py --lookback 200 --granularity 60 --product_id BTC-USD --output_file /tmp/cb_pro.json
```

With those arguments, you'll get 200 days worth of data at the hourly level, for the BTC-USD product.
The data will be written to ```tmp/cb_pro.json```.
You can adjust the arguments as needed.

The data will be written to the local file as new-line delimited json.
To read it into a dataframe, you can use:
```python
>>> import pandas as pd
>>> df = pd.read_json("/tmp/cb_pro.json", lines=True)
```

## Unit testing

We only have a couple tests at this point.
You can run them with ```make test```.
