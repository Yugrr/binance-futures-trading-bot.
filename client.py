"""
Direct REST client for Binance Futures Demo/Testnet.

We talk to the API directly with `requests` (one of the two approaches the
assignment explicitly allows) instead of the python-binance library, because
python-binance's built-in testnet=True mode still targets the old
testnet.binancefuture.com host and does not cleanly support Binance's
2025 "Demo Trading" domain (demo-fapi.binance.com), which caused
authentication errors even with valid keys.
"""

import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from bot.logging_config import get_logger

logger = get_logger(__name__)


class BinanceFuturesTestnetClient:
    # Binance revamped its Futures Testnet in late 2025 ("Demo Trading").
    # The web UI now lives at demo.binance.com, and the API base URL
    # changed accordingly from testnet.binancefuture.com to demo-fapi.binance.com.
    BASE_URL = "https://demo-fapi.binance.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("Initialized Binance Futures Demo/Testnet client")

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = 5000
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        logger.info(f"Placing order request: {params}")

        signed_params = self._sign(dict(params))
        url = f"{self.BASE_URL}/fapi/v1/order"

        response = self.session.post(url, params=signed_params, timeout=10)

        try:
            data = response.json()
        except ValueError:
            data = {"msg": response.text}

        if response.status_code != 200:
            logger.error(f"Order failed: {data}")
            raise Exception(data.get("msg", str(data)))

        logger.info(f"Order response: {data}")
        return data
