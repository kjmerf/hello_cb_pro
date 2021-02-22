import json
import logging
import requests

from cbt.utils.transaction import Transaction


def cb_post(url, data, auth):
    return requests.post(
        url,
        data=json.dumps(data),
        auth=auth,
        headers={"content-type": "application/json"},
    )


def get_accounts(url, auth):
    resp = requests.get(f"{url}/accounts", auth=auth)
    if resp.status_code == 200:
        valid_accounts = []
        for account in resp.json():
            if float(account["available"]) > 0:
                valid_accounts.append(account)
        return valid_accounts
    else:
        logging.error(f"GET failed: {resp.text}")


def market_order_btc(url, side, auth, size_or_funds, order_id, product="BTC-USD", max_requests=5):
    payload = {
        "client_oid": order_id,
        "product_id": product,
        "side": side,
        "type": "market",
    }
    if side == "buy":
        payload["funds"] = size_or_funds
    elif side == "sell":
        payload["size"] = size_or_funds
    else:
        raise ValueError(f"Expecting buy or sell but got {side}!")

    resp = cb_post(f"{url}/orders", payload, auth)

    if "Insufficient funds" in resp.text:
        log_insufficient_funds(side)
    elif resp.status_code == 200:
        # make sure the order went through
        logging.info(f"The market {side} order was submitted!")

        order = requests.get(f"{url}/orders/client:{order_id}", auth=auth)
        if order.status_code == 200:
            order_status = order.json()
            for i in range(max_requests):
                if order_status["settled"]:
                    transaction = log_order_settled(side, order_status)
                    return transaction
                else:
                    logging.info("Waiting for order to be fulfilled...")
                    order = requests.get(
                        f"{url}/orders/client:{order_id}", auth=auth
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
            "The API call succeeded but you have insufficient funds! You need to deposit some fake money in your CB sandbox account."
        )
    else:
        logging.warning(
            "The API call succeeded but you have insufficient BTC! You need to buy some BTC with your CB sandbox account."
        )


def log_order_settled(side, order_status):
    logging.info(f"Your market {side} was successful!")
    filled_size = order_status["filled_size"]
    fill_fees = float(order_status["fill_fees"])
    
    if side == "buy":
        usd = float(order_status["specified_funds"])
    else:
        usd = float(order_status["executed_value"]) 

    transaction = Transaction("", side, usd, filled_size, fill_fees)
    logging.info(transaction)
    return transaction
