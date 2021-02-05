# hello_cb_pro

This purpose of this repo is to explore the Coinbase Pro Sandbox API.
The Sandbox API mimics the production one.

## Setup

To use the repo, you first need to create an account here: https://public.sandbox.pro.coinbase.com.
Then create an API key associated with the account and set the following environment variables accordingly:
```CB_API_KEY```, ```CB_API_SECRET``` and ```CB_PASSPHRASE```.

## Running locally

Once the setup is complete, simply run ```/up.sh``` to start the container.
The container makes an authenticated and an unauthenticated call to the Sandbox API.
