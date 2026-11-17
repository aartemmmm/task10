import json
from io import BytesIO
from unittest.mock import Mock

import pytest

from seminar_shop.__main__ import ShopHandler


def checkout(**data):
    body = json.dumps(data).encode()
    headers = (
        "POST /orders/checkout HTTP/1.0\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
    ).encode()
    output = BytesIO()
    connection = Mock()
    connection.makefile.return_value = BytesIO(headers + body)
    connection.sendall.side_effect = output.write
    ShopHandler(connection, ("127.0.0.1", 0), None)
    response_headers, response_body = output.getvalue().split(b"\r\n\r\n", 1)
    return int(response_headers.split()[1]), json.loads(response_body)


def test_checkout_returns_total_and_normalized_email():
    status, body = checkout(unit_price=199, quantity=2, email=" shopper@example.com ")
    assert status == 200
    assert body == {"total": 398, "email": "shopper@example.com"}


@pytest.mark.parametrize(
    ("customer", "message"),
    [
        ({}, "Email is required"),
        ({"email": ""}, "Email is required"),
        ({"email": "shopper"}, "Enter an email such as user@example.com"),
        ({"email": 123}, "Email must be a string"),
    ],
)
def test_checkout_rejects_invalid_email(customer, message):
    status, body = checkout(unit_price=199, quantity=2, **customer)
    assert status == 400
    assert body == {"error": message}
