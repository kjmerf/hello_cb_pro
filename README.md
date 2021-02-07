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

## Running locally

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
