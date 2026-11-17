"""Run the classroom shop API."""

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .orders import order_total
from .registration import validate_email


class ShopHandler(BaseHTTPRequestHandler):
    def send_json(self, status: HTTPStatus, value: dict[str, object]) -> None:
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
        elif self.path == "/":
            self.send_json(
                HTTPStatus.OK,
                {"service": "seminar-shop", "endpoints": ["/health", "/register", "/orders/quote"]},
            )
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})

    def do_POST(self) -> None:
        if self.path not in {"/register", "/orders/quote"}:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 4096:
                raise ValueError("Body must be between 1 and 4096 bytes")
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            result: dict[str, object]
            if self.path == "/register":
                email = data.get("email")
                if not isinstance(email, str):
                    raise ValueError("Email must be a string")
                result = {"email": validate_email(email)}
            else:
                unit_price, quantity = data.get("unit_price"), data.get("quantity")
                if type(unit_price) is not int or type(quantity) is not int:
                    raise ValueError("Price and quantity must be integers")
                result = {"total": order_total(unit_price, quantity)}
        except ValueError as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        else:
            self.send_json(HTTPStatus.OK, result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), ShopHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
