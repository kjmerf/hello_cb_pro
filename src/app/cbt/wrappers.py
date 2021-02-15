import os
import requests
import json


rest_url = os.getenv("CB_REST_URL")


def market_buy_btc(auth, funds, product="BTC-USD"):

    payload = {"product_id": product, "side": "buy", "type": "market", "funds": funds}

    resp = requests.post(
        f"{rest_url}/orders",
        data=json.dumps(payload),
        auth=auth,
        headers={"content-type": "application/json"},
    )
    if "Insufficient funds" in resp.text:
        print(
            "The API call succeeded but you have insufficient funds! You just need to deposit some fake money in your CB sandbox account."
        )
    elif resp.status_code == 200:
        print(f"The buy order was submitted! Here is your receipt: {resp.json()}")
    else:
        print(resp.error)
