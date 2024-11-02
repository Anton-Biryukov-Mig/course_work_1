import datetime
import json
import logging
from typing import Dict, List

import pandas as pd
import requests


def get_greeting(date_time: datetime.datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Args:
        date_time (datetime.datetime): Текущее время.

    Returns:
        str: Приветствие.
    """
    logging.info("Определение приветствия")
    hour = date_time.hour
    if hour < 6:
        return "Доброй ночи"
    elif hour < 12:
        return "Доброе утро"
    elif hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_cards(data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, float]]:
    """
    Возвращает список карт с информацией о последних четырех цифрах номера карты, общей сумме трат и cashback.

    Args:
        data (Dict[str, List[Dict[str, str]]]): Данные о картах и транзакциях.

    Returns:
        List[Dict[str, float]]: Список карт с информацией.
    """
    logging.info("Получение информации о картах")
    cards = []
    for card in data["cards"]:
        last_digits = card["card_number"][-4:]
        transactions_df = pd.DataFrame(card["transactions"])
        total_spent = transactions_df["amount"].sum()
        cashback = total_spent * 0.01
        cards.append({"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback})
    return cards


def get_top_transactions(data: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    Возвращает список топ-5 транзакций по сумме трат.

    Args:
        data (Dict[str, List[Dict[str, str]]]): Данные о транзакциях.

    Returns:
        List[Dict[str, str]]: Список топ-5 транзакций.
    """
    logging.info("Получение топ-5 транзакций")
    transactions_df = pd.DataFrame(data["transactions"])
    transactions_df["Сумма операции"] = transactions_df["Сумма операции"].astype(float)
    top_transactions_df = transactions_df.nlargest(5, "Сумма операции")
    top_transactions = [
        {str(key): str(value) for key, value in row.items()} for row in top_transactions_df.to_dict("records")
    ]

    return top_transactions


def get_currency_rates(user_settings: Dict[str, List[str]]) -> List[Dict[str, float]]:
    """
    Возвращает список курсов валют.

    Args:
        user_settings (Dict[str, List[str]]): Настройки пользователя.

    Returns:
        List[Dict[str, float]]: Список курсов валют.
    """
    logging.info("Получение курсов валют")
    currency_rates = []
    for currency in user_settings["user_currencies"]:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
        data = response.json()
        currency_rates.append({"currency": currency, "rate": data["rates"][currency]})
    return currency_rates


def get_stock_prices(user_settings: Dict[str, List[str]]) -> List[Dict[str, object]]:
    """
    Возвращает список цен акций.
    Args:
        user_settings (Dict[str, List[str]]): Настройки пользователя.
    Returns:
        List[Dict[str, object]]: Список цен акций.
    """
    logging.info("Получение цен акций")
    stock_prices = []
    api_key = "02d04bda4326f77763e22e13426f9588"
    api_endpoint = "https://www.alphavantage.co/query"  # Replace with the actual API endpoint
    for stock in user_settings["user_stocks"]:
        params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": api_key}
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 (OK)
        data = response.json()
        try:
            stock_price = float(data["Global Quote"]["05. price"])
        except (KeyError, ValueError):
            stock_price = 0.0
        stock_prices.append({"stock": stock, "price": stock_price})
    return stock_prices


def get_json_response(
    date_time: datetime.datetime, data: Dict[str, List[Dict[str, str]]], user_settings: Dict[str, List[str]]
) -> str:
    """
    Возвращает JSON-ответ с информацией о приветствии, картах, топ-5 транзакциях, курсах валют и ценах акций.
    Args:
        date_time (datetime.datetime): Текущее время.
        data (Dict[str, List[Dict[str, str]]]): Данные о картах и транзакциях.
        user_settings (Dict[str, List[str]]): Настройки пользователя.
    Returns:
        str: JSON-ответ.
    """
    logging.info("Формирование JSON-ответа")
    greeting = get_greeting(date_time)
    cards = get_cards(data)
    top_transactions = get_top_transactions(data)
    currency_rates = get_currency_rates(user_settings)
    stock_prices = get_stock_prices(user_settings)
    return json.dumps(
        {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }
    )
