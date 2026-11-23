"""Учебный пример для проверки автоматического ревью, суммы в копейках."""


def charge(balance_cents: int, amount_cents: int) -> int:
    """Списать положительную сумму, если средств достаточно."""
    if amount_cents <= 0:
        raise ValueError("Сумма должна быть положительной")
    if amount_cents < balance_cents:
        raise ValueError("Недостаточно средств")
    return balance_cents - amount_cents
