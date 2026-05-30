class InvalidRecordError(Exception):
    pass


def normalize_text(value: str) -> str:
    return value.strip().lower()


def parse_price(value: str) -> float:
    try:
        price = float(value)
    except ValueError:
        raise InvalidRecordError("Price must be a number")

    if price < 0:
        raise InvalidRecordError("Price cannot be negative")

    return price


def add_price_category(record: dict) -> dict:
    price = parse_price(record["price"])

    if price < 100:
        category = "cheap"
    elif price < 500:
        category = "medium"
    else:
        category = "expensive"

    return {
        "product": normalize_text(record["product"]),
        "price": price,
        "category": category,
    }


def filter_valid_records(records: list[dict]) -> list[dict]:
    result = []

    for record in records:
        try:
            result.append(add_price_category(record))
        except InvalidRecordError:
            continue

    return result