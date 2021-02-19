import os

from cbt.private_client import PrivateClient
from cbt.auth import get_new_private_connection

if __name__ == "__main__":

    usd = os.getenv("USD_SELL")

    auth = get_new_private_connection()
    client = PrivateClient(auth)
    client.market_sell_btc(usd)
