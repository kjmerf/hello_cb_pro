import os
import requests
import json


rest_url = os.getenv("CB_REST_URL")


def cb_post(url, data, auth):
    return requests.post(
        url,
        data=json.dumps(data),
        auth=auth,
        headers={"content-type": "application/json"},
    )


def market_buy_btc(auth, funds, product="BTC-USD"):
    payload = {"product_id": product, "side": "buy", "type": "market", "funds": funds}
    resp = cb_post(f"{rest_url}/orders", payload, auth)

    if "Insufficient funds" in resp.text:
        print(
            "The API call succeeded but you have insufficient funds! You just need to deposit some fake money in your CB sandbox account."
        )
    elif resp.status_code == 200:
        print(f"The buy order was submitted! Here is your receipt: {resp.json()}")
    else:
        print(resp.text)


def market_sell_btc(auth, funds, product="BTC-USD"):
    payload = {"product_id": product, "side": "sell", "type": "market", "funds": funds}
    resp = cb_post(f"{rest_url}/orders", payload, auth)

    if "Insufficient funds" in resp.text:
        print(
            "The API call succeeded but you have insufficient funds! You just need to buy some BTC with your CB sandbox account."
        )
    elif resp.status_code == 200:
        print(f"The sell order was submitted! Here is your receipt: {resp.json()}")
    else:
        print(resp.text)

