import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_rate(currency_from, currency_to="RUB"):
    """Функция получения курса валюты"""
    if not isinstance(currency_from, str) or not isinstance(currency_to, str):
        raise ValueError("Коды валют должны быть строками")

    if len(currency_from) != 3 or len(currency_to) != 3:
        raise ValueError("Коды валют должны состоять из 3 символов")

    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency_to}&base={currency_from}"
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        result = response.json()
        if status_code == 200:
            return result['rates']
        else:
            return "Запрос отклонён. Причина: некорректные данные"
    except requests.exceptions.RequestException:
        print("Произошла ошибка. Проверьте корректность данных")

if __name__ == "__main__":
    print(get_rate("EUR"))
