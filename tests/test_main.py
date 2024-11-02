from typing import Dict, Hashable, List
from unittest.mock import MagicMock, patch

import pytest

from src.main import convert_to_str_dict, main


def test_convert_to_str_dict(mock_data: Dict[str, List[Dict[Hashable, str]]]) -> None:
    """Этот тест проверяет функцию convert_to_str_dict"""
    result = convert_to_str_dict(mock_data)
    assert result == {
        "cards": [],
        "transactions": [
            {"category": "Food", "amount": "100.0"},
            {"category": "Transport", "amount": "50.0"},
        ],
    }


@pytest.fixture
def mock_data() -> Dict[str, List[Dict[Hashable, str]]]:
    """Этот фикстура возвращает тестовые данные"""
    return {
        "cards": [],
        "transactions": [
            {"category": "Food", "amount": "100.0"},
            {"category": "Transport", "amount": "50.0"},
        ],
    }


@pytest.fixture
def mock_user_settings() -> Dict[str, List[str]]:
    """Этот фикстура возвращает тестовые настройки пользователя"""
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]}


@patch("src.views.get_json_response")
def test_main(
    mock_get_json_response: MagicMock,
    mock_data: Dict[str, List[Dict[Hashable, str]]],
    mock_user_settings: Dict[str, List[str]],
) -> None:
    """Этот тест проверяет функцию main"""
    mock_get_json_response.return_value = {}
    with patch("src.main.analyze_cashback_categories") as mock_analyze_cashback_categories:

        with patch("src.main.spending_by_category") as mock_spending_by_category:
            with patch("src.main.spending_by_weekday") as mock_spending_by_weekday:
                with patch("src.main.spending_by_workday") as mock_spending_by_workday:
                    main()

                    mock_analyze_cashback_categories.assert_called_once()

                    mock_spending_by_category.assert_called_once()
                    mock_spending_by_weekday.assert_called_once()
                    mock_spending_by_workday.assert_called_once()


@patch("src.services.analyze_cashback_categories")
def test_analyze_cashback_categories(
    mock_analyze_cashback_categories: MagicMock, mock_data: Dict[str, List[Dict[Hashable, str]]]
) -> None:
    """Этот тест проверяет функцию analyze_cashback_categories"""
    mock_analyze_cashback_categories.return_value = {}
    main()


@patch("src.reports.save_report_to_file_decorator")
def test_save_report_to_file_decorator(mock_save_report_to_file_decorator: MagicMock) -> None:
    """Этот тест проверяет функцию save_report_to_file_decorator"""
    mock_save_report_to_file_decorator.return_value = lambda x: x
    main()


@patch("src.reports.spending_by_category")
def test_spending_by_category(mock_spending_by_category: MagicMock) -> None:
    """Этот тест проверяет функцию spending_by_category"""
    mock_spending_by_category.return_value = {}
    main()


@patch("src.reports.spending_by_weekday")
def test_spending_by_weekday(mock_spending_by_weekday: MagicMock) -> None:
    """Этот тест проверяет функцию spending_by_weekday"""
    mock_spending_by_weekday.return_value = {}
    main()


@patch("src.reports.spending_by_workday")
def test_spending_by_workday(mock_spending_by_workday: MagicMock) -> None:
    """Этот тест проверяет функцию spending_by_workday"""
    mock_spending_by_workday.return_value = {}
    main()


if __name__ == "__main__":
    main()
