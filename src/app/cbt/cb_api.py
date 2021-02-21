import json
import logging
import requests


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
                    message = log_order_settled(side, order_status)
                    return message
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
        specified_funds = float(order_status["specified_funds"])
        message = f"You paid ${specified_funds:.2f}, which bought {filled_size} BTC and paid ${fill_fees:.2f} in fees"
        logging.info(message)
        return message
    else:
        executed_value = float(order_status["executed_value"])
        message = f"You sold {filled_size} BTC for ${executed_value:.2f} and paid ${fill_fees:.2f} in fees"
        logging.info(message)
        return message
