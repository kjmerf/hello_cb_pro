import json
import os
import requests


rest_url = os.getenv("CB_REST_URL")
max_requests = int(os.getenv("MAX_REQUESTS"))


def cb_post(url, data, auth):
    return requests.post(
        url,
        data=json.dumps(data),
        auth=auth,
        headers={"content-type": "application/json"},
    )


def market_order_btc(side, auth, funds, order_id, product="BTC-USD"):
    payload = {
        "client_oid": order_id,
        "product_id": product,
        "side": side,
        "type": "market",
        "funds": funds,
    }
    resp = cb_post(f"{rest_url}/orders", payload, auth)

    if "Insufficient funds" in resp.text:
        print_insufficient_funds(side)
    elif resp.status_code == 200:
        # make sure the order went through
        print(
            f"The market {side} order was submitted!"
        )  # Here is your receipt: {resp.json()}")

        order = requests.get(f"{rest_url}/orders/client:{order_id}", auth=auth)
        if order.status_code == 200:
            order_status = order.json()
            for i in range(max_requests):
                if order_status["settled"]:
                    print_order_settled(side, order_status)
                    return
                else:
                    print("Waiting for order to be fulfilled...")
                    order = requests.get(
                        f"{rest_url}/orders/client:{order_id}", auth=auth
                    )
                    order_status = order.json()
            print(f"Order was not fulfilled within {max_requests + 1} requests")
        else:
            print(f"GET failed: {order.text}")

    else:
        print(f"POST failed: {resp.text}")


def print_insufficient_funds(side):
    if side == "buy":
        print(
            "The API call succeeded but you have insufficient funds! You just need to deposit some fake money in your CB sandbox account."
        )
    else:
        print(
            "The API call succeeded but you have insufficient BTC! You just need to buy some BTC with your CB sandbox account."
        )


def print_order_settled(side, order_status):
    print(f"Your market {side} was successful!")
    if side == "buy":
        print(
            f"You paid ${float(order_status['specified_funds']):.2f}, which bought {order_status['filled_size']} BTC and paid ${float(order_status['fill_fees']):.2f} in fees"
        )
    else:
        print(
            f"You sold {order_status['filled_size']} BTC for ${float(order_status['specified_funds']):.2f} and paid ${float(order_status['fill_fees']):.2f} in fees"
        )
