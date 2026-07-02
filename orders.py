"""
Order placement logic: validates input, calls the client, and prints
a clear summary of what happened.
"""

from bot.client import BinanceFuturesTestnetClient
from bot.logging_config import get_logger
from bot.validators import validate_order_input

logger = get_logger(__name__)


class OrderService:
    def __init__(self, api_key, api_secret):
        self.client = BinanceFuturesTestnetClient(api_key, api_secret)

    def place_order(self, symbol, side, order_type, quantity, price=None):
        symbol, side, order_type, quantity, price = validate_order_input(
            symbol, side, order_type, quantity, price
        )

        print("\n--- Order Request Summary ---")
        print(f"Symbol   : {symbol}")
        print(f"Side     : {side}")
        print(f"Type     : {order_type}")
        print(f"Quantity : {quantity}")
        if order_type == "LIMIT":
            print(f"Price    : {price}")
        print("------------------------------\n")

        try:
            response = self.client.place_order(symbol, side, order_type, quantity, price)

            print("--- Order Response ---")
            print(f"Order ID     : {response.get('orderId')}")
            print(f"Status       : {response.get('status')}")
            print(f"Executed Qty : {response.get('executedQty')}")
            avg_price = response.get("avgPrice")
            if avg_price:
                print(f"Avg Price    : {avg_price}")
            print("SUCCESS: Order placed successfully!")
            print("----------------------\n")

            return response
        except Exception as e:
            print(f"FAILURE: Order could not be placed. Reason: {e}\n")
            logger.error(f"Order placement failed: {e}")
            return None
