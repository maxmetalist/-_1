import re


def filter_person_transfer(transactions):
    """Функция поиска переводов физ лицам"""
    name_pattern = re.compile(r"[А-ЯЁа-яё]+\s[А-ЯЁ]\.")

    filtered_transactions = []
    for transaction in transactions:
        if (
            transaction.get("Категория") == "Переводы"
            and transaction.get("Описание")
            and name_pattern.search(transaction["Описание"])
        ):
            filtered_transactions.append(
                {
                    "Дата операции": transaction.get("Дата операции"),
                    "Сумма операции": transaction.get("Сумма операции"),
                    "Валюта операции": transaction.get("Валюта операции"),
                    "Описание": transaction.get("Описание"),
                }
            )

    return filtered_transactions


def find_transactions_by_name(transactions, name):
    """Функция поиска транзакции по имени получателя в формате Иван П."""
    result = {}
    name_regex = re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE)

    for transaction in transactions:
        description = transaction.get("Описание", "")
        if name_regex.search(description):
            date = transaction.get("Дата операции")
            amount = transaction.get("Сумма платежа")

            if date and amount:
                result[date] = amount

    return result
