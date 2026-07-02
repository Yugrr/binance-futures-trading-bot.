# Simplified Trading Bot (Binance Futures Testnet)

A small Python CLI app that places MARKET and LIMIT orders (BUY/SELL) on
Binance Futures Testnet (USDT-M), with input validation, logging, and
error handling.

## Setup Steps

1. Install Python 3.9+ (check with `python --version` or `python3 --version`).
2. Clone/download this project and open a terminal inside the `trading_bot` folder.
3. (Recommended) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a Binance Futures Testnet account. Note: Binance revamped its
   testnet in late 2025 into "Demo Trading" — go to
   https://demo.binance.com/en/futures/BTCUSDT (the old
   testnet.binancefuture.com URL now leads here) and generate an API key +
   secret from the API Key section. The API base URL used by this bot is
   `https://demo-fapi.binance.com` accordingly.
6. Set your credentials as environment variables:
   ```
   export BINANCE_TESTNET_API_KEY="your_api_key"        # Mac/Linux
   export BINANCE_TESTNET_API_SECRET="your_api_secret"

   set BINANCE_TESTNET_API_KEY=your_api_key              # Windows (cmd)
   set BINANCE_TESTNET_API_SECRET=your_api_secret
   ```

## How to Run Examples

Place a MARKET order:
```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a LIMIT order:
```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

Each run prints:
- The order request summary
- The order response (orderId, status, executedQty, avgPrice if available)
- A success or failure message

## Logs

Every API request, response, and error is logged to `logs/trading_bot.log`.

## Assumptions

- This bot talks to Binance directly via REST calls using `requests`
  (one of the two allowed approaches) rather than the `python-binance`
  library. The library's built-in `testnet=True` mode still targets the
  old `testnet.binancefuture.com` host and produced authentication
  errors (`-2015 Invalid API-key`) against Binance's newer "Demo Trading"
  domain, even with valid keys — direct REST calls sidestep that.
- Binance's Futures Testnet UI/API moved from `testnet.binancefuture.com`
  to `demo.binance.com` / `demo-fapi.binance.com` (a late-2025 revamp
  Binance calls "Demo Trading"). This bot targets the current
  `demo-fapi.binance.com` endpoint, which is the live successor to the
  domain named in the assignment brief.
- Only USDT-M Futures Testnet is targeted (not Spot, not Coin-M).
- Only MARKET and LIMIT order types are implemented (core requirement);
  Stop-Limit/OCO/TWAP/Grid were left as optional bonus and not implemented
  here to keep the core solid.
- API credentials are read from environment variables rather than
  hardcoded or passed as CLI flags, to avoid leaking secrets in shell
  history or logs.
- LIMIT orders use `GTC` (Good-Til-Cancelled) as the time-in-force.

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance client wrapper
    orders.py           # order placement logic
    validators.py        # input validation
    logging_config.py    # logging setup
  cli.py                 # CLI entry point
  README.md
  requirements.txt
```
