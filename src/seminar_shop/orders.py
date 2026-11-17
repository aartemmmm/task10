"""Calculate order totals in integer cents."""

from .config import MAX_ORDER_QUANTITY


def order_total(unit_price: int, quantity: int) -> int:
    if unit_price < 0:
        raise ValueError("Price cannot be negative")
    if not 1 <= quantity <= MAX_ORDER_QUANTITY:
        raise ValueError(f"Quantity must be between 1 and {MAX_ORDER_QUANTITY}")
    return unit_price * quantity
