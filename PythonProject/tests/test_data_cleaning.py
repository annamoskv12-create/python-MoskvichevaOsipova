import pytest
from data_cleaning import (
    normalize_text,
    parse_price,
    add_price_category,
    filter_valid_records,
    InvalidRecordError,
)


# 1. Фикстура
@pytest.fixture
def raw_records():
    return [
        {"product": "  Laptop ", "price": "1200"},
        {"product": "Mouse  ", "price": "50"},
        {"product": "  Broken item  ", "price": "-10"},
        {"product": "Keyboard", "price": "abc"},
    ]


# 2. parametrize для normalize_text
@pytest.mark.parametrize(
    "raw_text, expected",
    [
        ("  Hello  ", "hello"),
        ("WORLD", "world"),
        ("  PyTest   ", "pytest"),
        ("", ""),
    ],
)
def test_normalize_text(raw_text, expected):
    assert normalize_text(raw_text) == expected


# 3. parametrize для parse_price с корректными значениями
@pytest.mark.parametrize(
    "price_str, expected_float",
    [
        ("10", 10.0),
        ("99.99", 99.99),
        ("0", 0.0),
        ("500.5", 500.5),
    ],
)
def test_parse_price_valid(price_str, expected_float):
    assert parse_price(price_str) == expected_float


# 4. pytest.raises для parse_price с неверными данными
@pytest.mark.parametrize(
    "bad_price",
    [
        "abc",
        "-100",
        "",
        "12.34.56",
        "one hundred",
    ],
)
def test_parse_price_raises_error(bad_price):
    with pytest.raises(InvalidRecordError):
        parse_price(bad_price)


# 5. Тестирование add_price_category (включая категории)
@pytest.mark.parametrize(
    "record, expected_category, expected_product, expected_price",
    [
        ({"product": "  cheap item  ", "price": "50"}, "cheap", "cheap item", 50.0),
        ({"product": "MEDIUM", "price": "250"}, "medium", "medium", 250.0),
        ({"product": "  Expensive  ", "price": "1000"}, "expensive", "expensive", 1000.0),
        ({"product": "  boundary  ", "price": "100"}, "medium", "boundary", 100.0),
        ({"product": "  boundary2  ", "price": "500"}, "expensive", "boundary2", 500.0),
    ],
)
def test_add_price_category(record, expected_category, expected_product, expected_price):
    result = add_price_category(record)
    assert result["category"] == expected_category
    assert result["product"] == expected_product
    assert result["price"] == expected_price


# 6. Тест с использованием фикстуры raw_records для filter_valid_records
def test_filter_valid_records(raw_records):
    filtered = filter_valid_records(raw_records)
    # Должны остаться только валидные записи: Laptop (1200), Mouse (50)
    assert len(filtered) == 2

    # Проверка первого очищенного элемента
    assert filtered[0]["product"] == "laptop"
    assert filtered[0]["price"] == 1200.0
    assert filtered[0]["category"] == "expensive"

    assert filtered[1]["product"] == "mouse"
    assert filtered[1]["price"] == 50.0
    assert filtered[1]["category"] == "cheap"


# 7. Пользовательская метка validation – проверка корректности parse_price
@pytest.mark.validation
def test_parse_price_validation_mark():
    assert parse_price("42") == 42.0
    with pytest.raises(InvalidRecordError):
        parse_price("-5")


# 8. Дополнительный тест на граничные условия для normalize_text
@pytest.mark.parametrize(
    "raw, expected",
    [
        ("\t tab \n", "tab"),
        ("  много   пробелов  ", "много   пробелов"),
    ],
)
def test_normalize_text_whitespace(raw, expected):
    assert normalize_text(raw) == expected


# 9. Проверка, что filter_valid_records возвращает пустой список, если все записи невалидны
def test_filter_valid_records_all_invalid():
    invalid_records = [
        {"product": "bad", "price": "-1"},
        {"product": "bad2", "price": "not a number"},
    ]
    assert filter_valid_records(invalid_records) == []
