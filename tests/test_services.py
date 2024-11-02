import datetime
from typing import Dict, List

import pytest


@pytest.fixture
def mock_data() -> Dict[str, List[Dict[str, str]]]:
    return {
        "transactions": [
            {"category": "Food", "amount": "100.0"},
            {"category": "Transport", "amount": "50.0"},
        ]
    }


def test_analyze_cashback_categories() -> None:
    """Этот тест проверяет функцию analyze_cashback_categories"""
    date_string = "01.01.2022 12:00:00"
    date_time = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")

    print(date_time)
