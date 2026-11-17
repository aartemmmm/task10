# Практическая № 10 — командная работа в GitHub

Пять заданий на примере учебного интернет-магазина на Python.

## Запуск магазина

Требуется Python 3.12 или новее. Установи зависимости в виртуальное окружение.

```sh
python -m pip install -r requirements-ci.txt
python -m pip install --no-deps --no-build-isolation .
python -m seminar_shop
```

## 1. Проверка email при оформлении заказа

`POST /orders/checkout` принимает цену в копейках, количество и email покупателя.

```sh
curl -sS -H 'Content-Type: application/json' \
  -d '{"unit_price":199,"quantity":2,"email":"shopper@example.com"}' \
  http://127.0.0.1:8080/orders/checkout
```

Ожидаемый ответ — `{"total":398,"email":"shopper@example.com"}`.

При пустом email API возвращает HTTP 400 и `Email is required`. При адресе
вроде `shopper` ответ тоже HTTP 400 с примером корректного адреса.
Пробелы по краям корректного адреса убираются.

```sh
python -m pytest tests/test_checkout.py -q
```
