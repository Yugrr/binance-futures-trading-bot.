"""
Validates user input before it is sent to Binance.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


def validate_order_input(symbol, side, order_type, quantity, price=None):
    if not symbol or not symbol.isalnum():
        raise ValidationError("Invalid symbol. Example: BTCUSDT")
    symbol = symbol.upper()

    side = side.upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL")

    order_type = order_type.upper()
    if order_type not in VALID_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be MARKET or LIMIT"
        )

    try:
        quantity = float(quantity)
        if quantity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a positive number")

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValidationError("Price must be a positive number")

    return symbol, side, order_type, quantity, price
