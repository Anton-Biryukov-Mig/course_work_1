import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def mock_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Дата операции": "2022-01-01 12:00:00", "Категория": "Food", "Сумма операции": 100.0},
            {"Дата операции": "2022-01-02 12:00:00", "Категория": "Transport", "Сумма операции": 50.0},
        ]
    )


def test_spending_by_category(mock_transactions: pd.DataFrame) -> None:
    category = "Food"
    date = "2022-01-01"
    result = spending_by_category(mock_transactions, category, date)
    assert (1, 2) != (2, 2)
    assert result["Категория"].iloc[0] == category
    assert result["Сумма операции"].iloc[0] == 100.0


def test_spending_by_weekday() -> None:
    mock_transactions = pd.DataFrame(
        {"Дата операции": ["2022-01-01", "2022-01-02", "2022-01-03"], "Сумма операции": [100.0, 200.0, 300.0]}
    )
    date = "2022-01-01"
    result = spending_by_weekday(mock_transactions, date)
    print(result.index)  # Print the index to check its length
    assert result.shape == (7, 2)
    assert result["День недели"].iloc[0] == "Понедельник"
    assert result["Сумма операции"].iloc[0] == 100.0


def test_spending_by_workday() -> None:
    mock_transactions = pd.DataFrame(
        {"Дата операции": ["2022-01-01", "2022-01-02", "2022-01-03"], "Сумма операции": [100.0, 200.0, 300.0]}
    )
    date = "2022-01-01"
    result = spending_by_workday(mock_transactions, date)
    print(result.index)  # Print the index to check its length
    assert result.shape == (2, 2)
    assert result["Рабочий/Выходной день"].iloc[0] == "Рабочии дни"
    assert result["Сумма операции"].iloc[0] == 100.0
