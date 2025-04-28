import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_RATE = os.getenv("RATE_API_KEY")
API_KEY_STOCK = os.getenv("STOCK_API_KEY")


def get_rate(currency_from, currency_to="RUB"):
    """Функция получения курса валюты"""
    if not isinstance(currency_from, str) or not isinstance(currency_to, str):
        raise ValueError("Коды валют должны быть строками")

    if len(currency_from) != 3 or len(currency_to) != 3:
        raise ValueError("Коды валют должны состоять из 3 символов")

    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency_to}&base={currency_from}"
        headers = {"apikey": API_KEY_RATE}
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        result = response.json()
        if status_code == 200:
            return result["rates"]
        else:
            return "Запрос отклонён. Причина: некорректные данные"
    except requests.exceptions.RequestException:
        print("Произошла ошибка. Проверьте корректность данных")


def get_stocks_price(symbol):
    """Функция получения котировок акций во временном интервале 60мин"""
    if isinstance(symbol, str) and symbol.isalpha():
        symbol = symbol.upper().strip()
        try:
            url = (
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
                f"{symbol}&interval=60min&apikey={API_KEY_STOCK}"
            )
            headers = {"apikey": API_KEY_STOCK}
            response = requests.get(url, headers=headers)
            status_code = response.status_code
            data = response.json()
            if status_code == 200:
                transformed = {
                    "symbol": data["Meta Data"]["2. Symbol"],
                    "price": {timestamp: data["4. close"] for timestamp, data in data["Time Series (60min)"].items()},
                }
                return transformed
            else:
                return "Запрос отклонён. Укажите параметры запроса"
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сервера: {e}")
            return {}
    else:
        return "Укажите символ требуемой котировки, например 'IBM'"
