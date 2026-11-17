import pytest

from seminar_shop.config import MAX_ORDER_QUANTITY
from seminar_shop.orders import order_total


def test_order_total_is_in_cents():
    assert order_total(199, 3) == 597


@pytest.mark.parametrize("quantity", [-1, MAX_ORDER_QUANTITY + 1])
def test_out_of_range_quantity(quantity):
    with pytest.raises(ValueError, match="Quantity"):
        order_total(199, quantity)


def test_maximum_quantity_is_accepted():
    assert order_total(1, MAX_ORDER_QUANTITY) == MAX_ORDER_QUANTITY


def test_negative_price_is_rejected():
    with pytest.raises(ValueError, match="Price"):
        order_total(-1, 1)
