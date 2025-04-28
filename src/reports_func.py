import datetime

from dateutil.relativedelta import relativedelta


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
