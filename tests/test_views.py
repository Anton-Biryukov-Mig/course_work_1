import datetime
from typing import Dict, List

import pytest

from src.views import get_cards, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions


@pytest.fixture
def mock_data() -> Dict[str, List[Dict[str, str]]]:
    return {
        "cards": [],
        "transactions": [
            {"category": "Food", "amount": "100.0"},
            {"category": "Transport", "amount": "50.0"},
        ],
    }


@pytest.fixture
def mock_user_settings() -> Dict[str, List[str]]:
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]}


def test_get_greeting() -> None:
    date_time = datetime.datetime(2022, 1, 1, 12, 0, 0)
    result = get_greeting(date_time)
    assert result == "Добрый день"


def test_get_cards(mock_data: Dict[str, List[Dict[str, str]]]) -> None:
    result = get_cards(mock_data)
    assert result == []


def test_get_top_transactions(mock_data: Dict[str, List[Dict[str, str]]]) -> None:
    mock_data["transactions"][0]["Сумма операции"] = "100.0"
    result = get_top_transactions(mock_data)
    assert len(result) == 2
    assert result[0]["category"] == "Food"
    assert result[0]["amount"] == "100.0"


def test_get_currency_rates(mock_user_settings: Dict[str, List[str]]) -> None:
    result = get_currency_rates(mock_user_settings)
    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] > 0


def test_get_stock_prices(mock_user_settings: Dict[str, List[str]]) -> None:
    result = get_stock_prices(mock_user_settings)
    assert len(result) == 2
    assert result[0]["stock"] == "AAPL"


def test_get_json_response(
    mock_data: Dict[str, List[Dict[str, str]]], mock_user_settings: Dict[str, List[str]]
) -> None:
    expected_response = (
        '{"greeting": "Добрый день", "cards": [], "top_transactions": '
        '[{"category": "Food", "amount": "100.0"}, '
        '{"category": "Transport", "amount": "50.0"}], "currency_rates": '
        '[{"currency": "USD", "rate": 1.0}, {"currency": "EUR", "rate": 0.9}], "stock_prices": '
        '[{"stock": "AAPL", "price": 100.0}, {"stock": "GOOG", "price": 200.0}]}'
    )

    assert expected_response
