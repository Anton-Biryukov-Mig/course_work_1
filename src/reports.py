import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, TypeAlias

import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = pd.read_excel(file_path)
transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Скрипт запущен")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает расходы по категории за последние три месяца.

    Args:
        transactions (pd.DataFrame): DataFrame с данными о транзакциях.
        category (str): Название категории.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Расходы по категории за последние три месяца.
    """
    logger.info(f"Категория: {category}, Дата {date}")
    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = pd.to_datetime(date, format="%d.%m.%Y")
    three_months_ago = date_obj - timedelta(days=90)
    logger.info(f"Расходы за последние три месяца: {three_months_ago}")
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= three_months_ago) & (transactions["Категория"] == category)
    ]
    spending = filtered_transactions.groupby("Категория")["Сумма операции"].sum().reset_index()
    spending["Сумма операции"] = spending["Сумма операции"].apply(lambda x: round(x))
    logger.info(f"Расходы по категории:\n " f"{spending}")
    return spending


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние расходы по дням недели за последние три месяца.

    Args:
        transactions (pd.DataFrame): DataFrame с данными о транзакциях.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Средние расходы по дням недели за последние три месяца.
    """
    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = pd.to_datetime(date, format="%d.%m.%Y")
    filtered_transactions = transactions[transactions["Дата операции"] >= (date_obj - timedelta(days=90))].copy()
    filtered_transactions.loc[:, "День недели"] = filtered_transactions["Дата операции"].dt.day_name()
    filtered_transactions.loc[:, "День недели"] = filtered_transactions["День недели"].apply(
        lambda x: {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }[x]
    )
    spending = filtered_transactions.groupby("День недели")["Сумма операции"].mean().reset_index()
    spending["День недели"] = spending["День недели"].apply(
        lambda x: {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6,
        }[x]
    )
    spending = spending.sort_values(by="День недели")
    spending["День недели"] = spending["День недели"].apply(
        lambda x: {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }[x]
    )
    spending["Сумма операции"] = spending["Сумма операции"].apply(lambda x: round(x))
    logger.info(f"Расходы по дням недели:\n " f"{spending}")
    return spending


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние расходы по типам дней за последние три месяца.

    Args:
        transactions (pd.DataFrame): DataFrame с данными о транзакциях.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Средние расходы по типам дней за последние три месяца.
    """
    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = pd.to_datetime(date, format="%d.%m.%Y")
    filtered_transactions = transactions[transactions["Дата операции"] >= (date_obj - timedelta(days=90))].copy()
    filtered_transactions.loc[:, "День недели"] = filtered_transactions["Дата операции"].dt.day_name()
    filtered_transactions.loc[:, "День недели"] = filtered_transactions["День недели"].apply(
        lambda x: {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }[x]
    )
    filtered_transactions.loc[:, "Рабочий/Выходной день"] = filtered_transactions["День недели"].apply(
        lambda x: "Рабочии дни" if x in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"] else "Выходные дни"
    )
    spending = filtered_transactions.groupby("Рабочий/Выходной день")["Сумма операции"].mean().reset_index()
    spending["Сумма операции"] = spending["Сумма операции"].apply(lambda x: round(x))
    spending = spending.sort_values(by="Рабочий/Выходной день", ascending=False)
    logger.info(f"Расходы по типам дней:\n " f"{spending}")
    return spending


def save_report_to_file(report: pd.DataFrame, filename: str = "report.json") -> None:
    """
    Сохраняет отчет в файл.

    Args:
        report (pd.DataFrame): Отчет для сохранения.
        filename (str, optional): Название файла для сохранения отчета. Defaults to "report.json".
    """
    logger.info(f"Сохранение отчета в файл: {filename}")
    report_json = report.to_json(orient="records")
    with open(filename, "w") as f:
        json.dump(json.loads(report_json), f, indent=4)
    logger.info(f"Отчет сохранен успешно: {filename}")


ReportFunc: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]


def save_report_to_file_decorator(filename: str = "report.json") -> Callable[[ReportFunc], ReportFunc]:
    """Декоратор для сохранения отчета в файл"""

    def decorator(func: ReportFunc) -> ReportFunc:
        def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
            report = func(*args, **kwargs)
            save_report_to_file(report, filename)
            return report

        return wrapper

    return decorator


if __name__ == "__main__":
    logger.info("Основная функция запущена")

    spending_by_category(transactions, "Каршеринг", "01.03.2022")
    spending_by_weekday(transactions, "01.03.2022")
    spending_by_workday(transactions, "01.03.2022")
    logger.info("Скрипт завершен")
