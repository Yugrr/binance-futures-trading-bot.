"""
CLI entry point for the trading bot.

Example usage:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import argparse
import os
import sys

from bot.orders import OrderService
from bot.validators import ValidationError


def get_credentials():
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        print(
            "ERROR: Please set BINANCE_TESTNET_API_KEY and "
            "BINANCE_TESTNET_API_SECRET environment variables."
        )
        sys.exit(1)

    return api_key, api_secret


def main():
    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures Testnet Trading Bot"
    )
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL", "buy", "sell"]
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "market", "limit"],
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument(
        "--price", required=False, help="Required only for LIMIT orders"
    )

    args = parser.parse_args()

    api_key, api_secret = get_credentials()
    service = OrderService(api_key, api_secret)

    try:
        service.place_order(
            args.symbol, args.side, args.order_type, args.quantity, args.price
        )
    except ValidationError as e:
        print(f"INPUT ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
