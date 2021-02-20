import csv

from cbt.private_client import PrivateClient
from cbt.auth import get_new_private_connection

if __name__ == "__main__":
    auth = get_new_private_connection()
    client = PrivateClient(auth)

    # TODO: client.load_candles()
    client.record_balances()
    # TODO: client.make_transaction() # and record it