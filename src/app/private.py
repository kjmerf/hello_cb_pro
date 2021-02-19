from pprint import pprint

from cbt.auth import get_new_private_connection
from cbt.private_client import PrivateClient

# https://docs.pro.coinbase.com/#private

if __name__ == "__main__":

    auth = get_new_private_connection()
    client = PrivateClient(auth)
    accounts = client.get_accounts()
    pprint(accounts.json())
