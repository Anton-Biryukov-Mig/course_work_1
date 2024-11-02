import datetime
import json
import logging
import os
import sys
from typing import Dict, Hashable, List, TypedDict

import pandas as pd

from src.reports import save_report_to_file_decorator, spending_by_category, spending_by_weekday, spending_by_workday
from src.services import analyze_cashback_categories
from src.views import get_json_response

sys.path.insert(0, "../src")


class StrDict(TypedDict):
    key: str
    value: str


def convert_to_str_dict(data: Dict[str, List[Dict[Hashable, str]]]) -> Dict[str, List[Dict[str, str]]]:
    if data is None:
        raise TypeError("Data cannot be None")
    result = {}
    for key, value in data.items():
        result[key] = [{str(k): str(v) for k, v in item.items()} for item in value]
    return result


def main() -> None:
    """
    Основная функция программы.
    В этой функции происходит чтение данных из файла operations.xlsx, загрузка настроек пользователя из
    файла user_settings.json,
    получение JSON-ответа с информацией о приветствии, картах, топ-5 транзакциях, курсах валют и ценах акций,
    а также анализ категорий кэшбэка для заданного года и месяца.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Начало работы программы")

    date_time = datetime.datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
    logger.info(f"Текущая дата и время: {date_time}")

    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
    data = pd.read_excel(file_path)
    logger.info("Данные из файла operations.xlsx прочитаны успешно")

    file_path = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
    with open(file_path, "r") as f:
        user_settings = json.load(f)
    logger.info("Настройки пользователя загружены успешно")

    data_dict: Dict[str, List[Dict[str, str]]] = convert_to_str_dict(
        {"cards": [], "transactions": [{str(k): str(v) for k, v in row.items()} for row in data.to_dict("records")]}
    )
    json_response = get_json_response(date_time, data_dict, user_settings)
    logger.info("JSON-ответ получен успешно")
    print(json_response)

    year = 2022
    month = 1
    data_dict_2: Dict[str, List[Dict[str, str]]] = convert_to_str_dict({"transactions": data.to_dict("records")})
    cashback_categories = analyze_cashback_categories(data_dict_2, year, month)
    logger.info("Анализ категорий кэшбэка завершен успешно")
    print(cashback_categories)

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    transactions = pd.read_excel(os.path.join(data_dir, "operations.xlsx"))
    spending_by_category_report = spending_by_category(transactions, "Каршеринг", "2022-03-01")
    spending_by_weekday_report = spending_by_weekday(transactions, "2022-03-01")
    spending_by_workday_report = spending_by_workday(transactions, "2022-03-01")
    save_report_to_file_decorator("spending_by_category.json")(spending_by_category_report)
    save_report_to_file_decorator("spending_by_weekday.json")(spending_by_weekday_report)
    save_report_to_file_decorator("spending_by_workday.json")(spending_by_workday_report)

    logger.info("Программа завершена успешно")


if __name__ == "__main__":
    main()
