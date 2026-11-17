"""A deliberately small email rule for the classroom example."""

import re

EMAIL_PATTERN = re.compile(r"[^\s@.]+(?:\.[^\s@.]+)*@[^\s@.]+(?:\.[^\s@.]+)+")


def validate_email(email: str) -> str:
    address = email.strip()
    if not address:
        raise ValueError("Email is required")
    if not EMAIL_PATTERN.fullmatch(address):
        raise ValueError("Enter an email such as user@example.com")
    return address
