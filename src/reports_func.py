import datetime
import os

from dateutil.relativedelta import relativedelta

from src.xlsx_reader import read_xlsx_transactions


def filter_transactions_by_category(transactions, category, date=None):
    """Фильтрует транзакции по категории за последние 3 месяца от указанной даты"""
    if date:
        reference_date = datetime.datetime.strptime(date, "%d.%m.%Y").date()
    else:
        reference_date = datetime.date.today()

    three_months_ago = reference_date - relativedelta(months=3)

    filtered_transactions = []

    for transaction in transactions:
        if transaction.get("Категория") != category:
            continue

        try:
            op_date_str = transaction["Дата операции"].split()[0]
            op_date = datetime.datetime.strptime(op_date_str, "%d.%m.%Y").date()
        except (KeyError, ValueError):
            continue

        if three_months_ago <= op_date <= reference_date:
            filtered_transactions.append(transaction)

    return filtered_transactions


if __name__ == "__main__":
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
    transacts = read_xlsx_transactions(transactions_path)
    print(filter_transactions_by_category(transacts, "Переводы", "20.03.2020"))
