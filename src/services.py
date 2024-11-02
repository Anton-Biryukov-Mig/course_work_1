import datetime
import json
import logging
from typing import Dict, List


def analyze_cashback_categories(data: Dict[str, List[Dict[str, str]]], year: int, month: int) -> str:
    """
    Анализирует категории кэшбэка за указанный год и месяц.

    Аргументы:
        data (Dict[str, List[Dict[str, str]]]): Данные, содержащие транзакции.
        year (int): Год, за который необходимо проанализировать категории кэшбэка.
        month (int): Месяц, за который необходимо проанализировать категории кэшбэка.

    Возвращает:
        str: JSON-строка, содержащая категории кэшбэка.
    """
    logging.info(f"Анализируются категории кэшбэка за {year}-{month:02d}")
    categories: Dict[str, float] = {}
    for transaction in data["transactions"]:
        transaction_date = datetime.datetime.strptime(
            transaction["\u0414\u0430\u0442\u0430 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438"],
            "%d.%m.%Y %H:%M:%S",
        )
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["category"]
            amount = float(transaction["amount"])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount
    cashback_categories: Dict[str, float] = {}
    for category, amount in categories.items():
        cashback = amount * 0.01
        cashback_categories[category] = cashback
    logging.info(f"Категории кэшбэка проанализированы: {cashback_categories}")
    return json.dumps(cashback_categories)
