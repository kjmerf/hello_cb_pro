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
            "Congratulations! The transaction went through. You just need to deposit some fake money in your CB sandbox account."
        )
    else:
        print(f"Possibly 'bought' ${funds} of BTC. Check the CB pro UI!")
