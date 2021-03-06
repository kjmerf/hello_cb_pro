import base64
import hashlib
import hmac
import time

from requests.auth import AuthBase
import psycopg2


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = "".join(
            [
                timestamp,
                request.method,
                request.path_url,
                (request.body or b"".decode()),
            ]
        )
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update(
            {
                "CB-ACCESS-SIGN": signature_b64,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-ACCESS-KEY": self.api_key,
                "CB-ACCESS-PASSPHRASE": self.passphrase,
                "Content-Type": "application/json",
            }
        )
        return request


def get_cb_auth(api_key, api_secret, passphrase):
    return CoinbaseExchangeAuth(api_key, api_secret, passphrase)


def get_pg_conn(host, database, user, password, port=25060):
    return psycopg2.connect(
        host=host, database=database, user=user, password=password, port=port
    )
