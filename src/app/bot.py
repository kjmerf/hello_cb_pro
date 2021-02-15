from datetime import datetime
import logging
import os

import requests

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


if __name__ == "__main__":

    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    rest_url = os.getenv("CB_REST_URL")
    slack_channel = os.getenv("SLACK_CHANNEL")
    product_id = os.getenv("PRODUCT_ID")

    cb_response = requests.get(f"{rest_url}/products/{product_id}/stats",)
    logging.info(f"Status code from {rest_url}: {cb_response.status_code}")

    message = [
        f":moneybag: *{product_id} 24 Hour Stats*",
        f"*time*: {datetime.utcnow().isoformat()}",
    ]
    for k, v in cb_response.json().items():
        message.append(f"*{k}*: {round(float(v), 2)}")

    slack_response = requests.post(
        "https://slack.com/api/chat.postMessage",
        data={
            "token": slack_bot_token,
            "channel": slack_channel,
            "text": "\n\t".join(message),
            "as_user": True,
        },
    )
    logging.info(f"Status code from slack: {slack_response.status_code}")
