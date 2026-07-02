"""
Diagnostic script: checks if your API key/secret can authenticate with
Binance Futures Demo/Testnet at all, without placing any order.

Run:
    python check_connection.py
"""

import hashlib
import hmac
import os
import sys
import time
from urllib.parse import urlencode

import requests

BASE_URL = "https://demo-fapi.binance.com"


def main():
    api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
    api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        print("ERROR: BINANCE_TESTNET_API_KEY / BINANCE_TESTNET_API_SECRET not set.")
        sys.exit(1)

    print(f"API key starts with: {api_key[:6]}... (length {len(api_key)})")
    print(f"Secret starts with:  {api_secret[:6]}... (length {len(api_secret)})")

    # Step 1: public endpoint, no auth needed - just checks connectivity
    print("\n[1/2] Checking server time (no auth needed)...")
    r = requests.get(f"{BASE_URL}/fapi/v1/time", timeout=10)
    print(f"Status: {r.status_code}  Response: {r.text}")

    # Step 2: signed/private endpoint - this is the real auth test
    print("\n[2/2] Checking account balance (requires valid API key)...")
    params = {"timestamp": int(time.time() * 1000), "recvWindow": 5000}
    query_string = urlencode(params)
    signature = hmac.new(
        api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    params["signature"] = signature

    r = requests.get(
        f"{BASE_URL}/fapi/v2/balance",
        params=params,
        headers={"X-MBX-APIKEY": api_key},
        timeout=10,
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

    if r.status_code == 200:
        print("\nSUCCESS: Your API key is working correctly!")
    else:
        print("\nFAILURE: Authentication problem - see response above for the reason.")


if __name__ == "__main__":
    main()
