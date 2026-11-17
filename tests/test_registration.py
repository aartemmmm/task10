import pytest

from seminar_shop.registration import validate_email


def test_valid_email_is_trimmed():
    assert validate_email("  customer+shop@example.com  ") == "customer+shop@example.com"


@pytest.mark.parametrize("email", ["", "   "])
def test_empty_email(email):
    with pytest.raises(ValueError, match="Email is required"):
        validate_email(email)


@pytest.mark.parametrize(
    "email", ["name", "a@@example.com", "user@example", "user@exa mple.com", ".user@example.com"]
)
def test_invalid_email(email):
    with pytest.raises(ValueError, match="Enter an email"):
        validate_email(email)
