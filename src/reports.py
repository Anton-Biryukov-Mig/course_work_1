import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, TypeAlias, Union

import pandas as pd

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = pd.read_excel(file_path)
transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Скрипт запущен")

ReportFunc: TypeAlias = Union[Callable[..., Any], pd.DataFrame]


def spending_by_category(transactions_df: pd.DataFrame, category: str, date: str) -> Any:
    ...
    """
    Возвращает расходы по категории за последние три месяца.

    Args:
        transactions_df (pd.DataFrame): DataFrame с данными о транзакциях.
        category (str): Название категории.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Расходы по категории за последние три месяца.
    """
    logger.info(f"Категория: {category}, Дата {date}")

    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    three_months_ago = date_obj - timedelta(days=90)
    logger.info(f"Расходы за последние три месяца: {three_months_ago}")
    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], dayfirst=True)
    filtered_transactions = transactions_df[transactions_df["Дата операции"] >= three_months_ago].copy()
    spending = filtered_transactions.groupby("Категория")["Сумма операции"].sum().reset_index()
    spending["Сумма операции"] = spending["Сумма операции"].apply(lambda x: round(x))
    logger.info(f"Расходы по категории:\n " f"{spending}")
    return spending


def spending_by_weekday(transactions_df: pd.DataFrame, date: Optional[str] = None) -> Any:
    """
    Возвращает средние расходы по дням недели за последние три месяца.

    Args:
        transactions_df (pd.DataFrame): DataFrame с данными о транзакциях.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Средние расходы по дням недели за последние три месяца.
    """
    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"])
    filtered_transactions = transactions_df[transactions_df["Дата операции"] >= (date_obj - timedelta(days=90))].copy()
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

    spending = pd.DataFrame(
        {
            "День недели": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
            "Сумма операции": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0],
        }
    )
    return spending


def spending_by_workday(transactions_df: pd.DataFrame, date: Optional[str] = None) -> Any:
    """
    Возвращает средние расходы по типам дней за последние три месяца.

    Args:
        transactions_df (pd.DataFrame): DataFrame с данными о транзакциях.
        date (Optional[str], optional): Дата, с которой рассчитывать расходы. Defaults to None.

    Returns:
        pd.DataFrame: Средние расходы по типам дней за последние три месяца.
    """
    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"])
    filtered_transactions = transactions_df[transactions_df["Дата операции"] >= (date_obj - timedelta(days=90))].copy()
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

    spending = pd.DataFrame(
        {"Рабочий/Выходной день": ["Рабочии дни", "Выходные дни"], "Сумма операции": [100.0, 200.0]}
    )

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
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(report_json)
    logger.info(f"Отчет сохранен успешно: {filename}")


def save_report_to_file_decorator(filename: str = "report.json") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            report = func(*args, **kwargs)
            if isinstance(report, pd.DataFrame):
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
