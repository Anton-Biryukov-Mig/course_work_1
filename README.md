# Анализ транзакций
## Проект для анализа транзакций из Excel-файла.

## Функциональность
- Генерация JSON-данных для веб-страниц
- Формирование Excel-отчетов
- Сервисы для анализа транзакций



## Структура проекта
- src: исходный код проекта
- data: Excel-файл с транзакциями
- tests: тесты для проекта
- user_settings.json: файл с пользовательскими настройками

## Установка и запуск
- Клонировать репозиторий
```
```
- Установить зависимости с помощью 
```
pip: pip install -r requirements.txt
```
- Запустить проект с помощью команды 
```
python main.py
```

## Использование
- Для генерации JSON-данных для веб-страниц используйте функцию views.main
- Для формирования Excel-отчетов используйте функцию reports.main
- Для использования сервисов анализа транзакций используйте функции из модуля services

## Тестирование:

- Написаны тесты к функциональностям проекта.
- Функциональный код покрыт тестами на 80% и более.
- При запуске тестов командой pytest все тесты завершаются успешно.
- Тесты используют Mock и patch.
- Тесты используют фикстуры для генерации тестовых данных.
- Тесты параметризированы.

## Данные

- Ссылка на Excel-файл c транзакциями: [operations.xlsx].

## Описание данных

- Дата операции — дата, когда произошла транзакция.
- Дата платежа — дата, когда был произведен платеж.
- Номер карты — последние 4 цифры номера карты.
- Статус — статус операции (например, OK, FAILED).
- Сумма операции — сумма транзакции в оригинальной валюте.
- Валюта операции — валюта, в которой была произведена транзакция.
- Сумма платежа — сумма транзакции в валюте счета.
- Валюта платежа — валюта счета.
- Кешбэк — размер полученного кешбэка.
- Категория — категория транзакции.
- MCC — код категории транзакции (соответствует международной классификации).
- Описание — описание транзакции.
- Бонусы (включая кешбэк) — количество полученных бонусов (включая кешбэк).
- Округление на «Инвесткопилку» — сумма, которая была округлена и переведена на «Инвесткопилку».
- Сумма операции с округлением — сумма транзакции, округленная до ближайшего целого числа.

## Авторы
[Anton Biryukov](https://github.com/Anton-Biryukov-Mig)

## Лицензия
MIT License#   c o u r s e - w o r k - 1  
 