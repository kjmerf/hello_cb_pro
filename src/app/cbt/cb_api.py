import json
import logging
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

def get_accounts(auth):
    resp = requests.get(f"{rest_url}/accounts", auth=auth)
    if resp.status_code == 200:
        valid_accounts = []
        for account in resp.json():
            if float(account['available']) > 0:
                valid_accounts.append(account)
        return valid_accounts
    else: 
        logging.error(f"GET failed: {resp.text}")

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
        log_insufficient_funds(side)
    elif resp.status_code == 200:
        # make sure the order went through
        logging.info(f"The market {side} order was submitted!")

        order = requests.get(f"{rest_url}/orders/client:{order_id}", auth=auth)
        if order.status_code == 200:
            order_status = order.json()
            for i in range(max_requests):
                if order_status["settled"]:
                    log_order_settled(side, order_status)
                    return
                else:
                    logging.info("Waiting for order to be fulfilled...")
                    order = requests.get(
                        f"{rest_url}/orders/client:{order_id}", auth=auth
                    )
                    order_status = order.json()
            logging.error(f"Order was not fulfilled within {max_requests + 1} requests")
        else:
            logging.error(f"GET failed: {order.text}")

    else:
        logging.error(f"POST failed: {resp.text}")


def log_insufficient_funds(side):
    if side == "buy":
        logging.warning(
            "The API call succeeded but you have insufficient funds! You just need to deposit some fake money in your CB sandbox account."
        )
    else:
        logging.warning(
            "The API call succeeded but you have insufficient BTC! You just need to buy some BTC with your CB sandbox account."
        )


def log_order_settled(side, order_status):
    logging.info(f"Your market {side} was successful!")
    if side == "buy":
        logging.info(
            f"You paid ${float(order_status['specified_funds']):.2f}, which bought {order_status['filled_size']} BTC and paid ${float(order_status['fill_fees']):.2f} in fees"
        )
    else:
        logging.info(
            f"You sold {order_status['filled_size']} BTC for ${float(order_status['specified_funds']):.2f} and paid ${float(order_status['fill_fees']):.2f} in fees"
        )
