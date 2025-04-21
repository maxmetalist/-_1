import datetime
from collections import Counter
import os
from src.xlsx_reader import read_xlsx_transactions
def get_current_time_string():
    current_date_time = datetime.datetime.now()
    time_string = current_date_time.strftime("%H:%M:%S")
    time_hour = time_string[:2]
    return time_hour

print(get_current_time_string())


def total_consume_card_number(transact):
    card_number_list = []
    card_amount = 0.0
    card_dict = {}
    for transaction in transact:
        if transaction.get("Статус") == "OK" and transaction.get("Номер карты"):
            card_number_list.append(transaction)
    for transaction in card_number_list:
        if "-" in transaction.get("Сумма платежа"):
            card_amount += round(float(transaction["Сумма платежа"]),2)
        card_dict[transaction.get("Номер карты")] = card_amount

    # card_list = []
    # card_dict = {}
    # for transaction in transact:
    #     for key, value in transaction.items():
    #         if key == "Номер карты":
    #             card_list.append(value)
    #
    # for el in card_list:
    #     for transaction in transact:
    #         if transaction["Статус"] == "FAILED":
    #             continue
    #         else:
    #             if el == transaction.get("Номер карты"):
    #                 card_dict[el] = transaction["Сумма платежа"]
    return card_dict
if __name__ == "__main__":
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
    transactions = read_xlsx_transactions(transactions_path)
    print(total_consume_card_number(transactions))
