import datetime
import json
import os

from src.api_external import get_rate, get_stocks_price
from src.reports_func import filter_transactions_by_category
from src.servises import filter_person_transfer, find_transactions_by_name
from src.utils import filter_transactions_by_current_month
from src.views import get_top5_transactions, total_consume_card_number
from src.xlsx_reader import read_xlsx_transactions


def main(current_time=None):
    now = current_time if current_time else datetime.datetime.now()
    current_hour = now.hour

    if 5 <= current_hour < 12:
        print("Доброе утро!")
    elif 12 <= current_hour < 18:
        print("Добрый день!")
    elif 18 <= current_hour < 23:
        print("Добрый вечер!")
    else:
        print("Доброй ночи!")

    while True:
        user_input_date = (
            input("Введите дату, до которой включительно провести выборку транзакций в формате дд.мм.гггг ")
            .lower()
            .strip()
        )
        if user_input_date:
            transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
            transactions = read_xlsx_transactions(transactions_path)
            transactions_filtered_by_user_month = filter_transactions_by_current_month(transactions, user_input_date)
            if transactions_filtered_by_user_month:
                print(
                    f"Список транзакций до {user_input_date} включительно:"
                    f"\n{json.dumps(transactions_filtered_by_user_month, indent=4, ensure_ascii=False)}"
                )
            else:
                print("Ничего не нашлось на этот период")
            break

    print("Посчитать траты за текущий месяц по номерам карт? Введите y/n")
    while True:
        user_input_cards = input().lower().strip()
        if user_input_cards == "y":
            filtered_transactions_by_card = total_consume_card_number(transactions_filtered_by_user_month)
            print(
                f"Список трат за текущий месяц до {user_input_date} по номерам карт:"
                f"\n{json.dumps(filtered_transactions_by_card, indent=4, ensure_ascii=False)}"
            )
            break
        elif user_input_cards == "n":
            break
        else:
            print("Введите y/n")

    print("Вывести топ 5 транзакций за текущий месяц? Введите y/n")
    while True:
        user_input_top5 = input().lower().strip()
        if user_input_top5 == "y":
            top5_transactions = get_top5_transactions(transactions_filtered_by_user_month)
            if top5_transactions:
                print(
                    f"Список пяти наибольших транзакций за текущий месяц до {user_input_date} включительно:"
                    f"\n{json.dumps(top5_transactions, indent=4, ensure_ascii=False)}"
                )
            else:
                print("Ничего не нашлось за этот период")
            break
        elif user_input_top5 == "n":
            break
        else:
            print("Введите y/n")

    print("Показать курс валюты на сегодняшний день? Введите y/n")
    while True:
        user_input_curr = input().lower().strip()
        if user_input_curr == "y":
            while True:
                user_input_currency_to = (
                    str(input("Введите обозначение валюты, от которой искать курс(по умолчанию будет взят RUB "))
                    .upper()
                    .strip()
                )
                user_input_currency_from = (
                    str(input("Введите обозначение валюты, по отношению к которой искать курс ")).upper().strip()
                )
                if user_input_currency_to.isalpha() and user_input_currency_from.isalpha():
                    print(
                        f"Курс {user_input_currency_to} к {user_input_currency_from} на сегодняшний день:"
                        f"\n{json.dumps(get_rate(user_input_currency_from,
                                                 user_input_currency_to), indent=4, ensure_ascii=False)}"
                    )
                    break
                elif user_input_currency_from.isalpha() and not user_input_currency_to:
                    print(
                        f"Курс RUB к {user_input_currency_from} на сегодняшний день:"
                        f"\n{json.dumps(get_rate(user_input_currency_from), indent=4, ensure_ascii=False)}"
                    )
                    break
                else:
                    print("Нужно ввести как минимум один параметр валюты( по отношению к которой искать курс)")
            break
        elif user_input_curr == "n":
            break
        else:
            print("Введите y или n")

    print("Показать список цен на акции? Введите y/n")
    while True:
        user_input_stock = input().lower().strip()
        if user_input_stock == "y":
            while True:
                user_input_stock_symbol = str(input("Введите символ требуемой акции(на латинице)")).upper().strip()
                if user_input_stock_symbol.isalpha():
                    print(
                        f"Список изменений котировки акций {user_input_stock_symbol} за сегодняшний день:"
                        f"\n{json.dumps(get_stocks_price(user_input_stock_symbol), indent=4, ensure_ascii=False)}"
                    )
                    break
                else:
                    print("Введите корректное обозначение акции, например IBM, AAPL, GOOGL")
            break
        elif user_input_stock == "n":
            break
        else:
            print("Введите y или n")

    print("Искать переводы физ лицам? Введите y/n")
    while True:
        user_input_fis = input().lower().strip()
        if user_input_fis == "y":
            trans_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
            trans = read_xlsx_transactions(trans_path)
            filtered_by_person = filter_person_transfer(trans)
            if filtered_by_person:
                print(f"Список переводов физ лицам:\n{json.dumps(filtered_by_person, indent=4, ensure_ascii=False)}")
            else:
                print("Ничего не нашлось в категории 'Переводы'")
            break
        elif user_input_fis == "n":
            break
        else:
            print("Введите y или n")

    print("Искать по имени получателя? Введите y/n")
    while True:
        user_input_name_yes = input().lower().strip()
        if user_input_name_yes == "y":
            while True:
                user_input_name = input("Введите имя получателя с большой буквы ")
                if user_input_name:
                    path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
                    trans_list = read_xlsx_transactions(path)
                    filtered_by_name = find_transactions_by_name(trans_list, user_input_name)
                    if filtered_by_name:
                        print(
                            f"Список транзакций получателю {user_input_name}:"
                            f"\n{json.dumps(filtered_by_name, indent=4, ensure_ascii=False)}"
                        )
                    else:
                        print("Ничего не нашлось по этому имени")
                    break
            break
        elif user_input_name_yes == "n":
            break
        else:
            print("Введите y или n")

    print("Показать список трат по категориям?")
    while True:
        user_input_cat = input().lower().strip()
        if user_input_cat == "y":
            trans_path_ = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
            trans_ = read_xlsx_transactions(trans_path_)
            while True:
                user_input_category = str(input("Введите название категории ")).title().strip()
                user_input_date_cat = input(
                    "Введите дату, до которой искать транзакции(выведется за последние три месяца до указанной даты "
                ).strip()
                filtered_transactions_by_category = filter_transactions_by_category(
                    trans_, user_input_category, user_input_date_cat
                )
                if filtered_transactions_by_category:
                    print(
                        f"Список транзакций в категории {user_input_category}"
                        f"за последние три месяца до {user_input_date_cat}:"
                        f"{json.dumps(filtered_transactions_by_category, indent=4, ensure_ascii=False)}"
                    )
                else:
                    print("Ничего не нашлось по этим параметрам")
                exit()
        elif user_input_cat == "n":
            break
        else:
            print("Введите y или n")


if __name__ == "__main__":
    print(main())
