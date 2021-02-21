import logging

import requests


def post_to_channel(slack_bot_token, slack_channel, message):

    slack_response = requests.post(
        "https://slack.com/api/chat.postMessage",
        data={
            "token": slack_bot_token,
            "channel": slack_channel,
            "text": message,
            "as_user": True,
        },
    )
    logging.info(f"Status code from slack: {slack_response.status_code}")
