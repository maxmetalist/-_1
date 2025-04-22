import datetime
import os
from src.xlsx_reader import read_xlsx_transactions
import logging
logger_utils = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "utils.log"), mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s %(lineno)d")
file_handler.setFormatter(file_formatter)
logger_utils.addHandler(file_handler)
logger_utils.setLevel(logging.DEBUG)

def get_current_time_string(timezone="Europe/Moscow"):
    """Функция получения текущего времени суток"""
    try:
        logger_utils.debug("Получение текущей даты")
        current_date_time = datetime.datetime.now()
        return current_date_time.strftime("%H")
    except Exception as e:
        logger_utils.error(f"Ошибка {e}")
        return datetime.datetime.utcnow().strftime("%H")

print(get_current_time_string())

from datetime import datetime
def filter_transactions_by_current_month(transactions, current_date=None):
    """Фильтрует транзакции с начала месяца по указанную дату"""
    if current_date is None:
        logger_utils.debug("Дата не задана, выбираем текущую дату")
        current_date = datetime.now()
    elif isinstance(current_date, str):
        logger_utils.debug("форматирование даты в формат дд.мм.гггг")
        current_date = datetime.strptime(current_date, '%d.%m.%Y')
    logger_utils.debug("Получение даты начала отчётного периода")
    first_day_of_month = current_date.replace(day=1)
    logger_utils.debug("Получение даты окончания отчётного периода")
    end_of_day = current_date.replace(hour=23, minute=59, second=59)

    filtered_transactions = []
    logger_utils.debug("Фильтрация транзакций по отчётному периоду")
    for transaction in transactions:
        try:
            op_date_str = transaction['Дата операции']
            op_date = datetime.strptime(op_date_str, '%d.%m.%Y %H:%M:%S')

            if first_day_of_month <= op_date <= end_of_day:
                filtered_transactions.append(transaction)

        except (KeyError, ValueError) as e:
            continue
    logger_utils.debug("Сортировка по убыванию даты в отфильтрованных транзакциях")
    filtered_transactions.sort(key=lambda x: datetime.strptime(x['Дата операции'], '%d.%m.%Y %H:%M:%S'))
    logger_utils.debug("Вывод результата")
    return filtered_transactions

if __name__ == "__main__":
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
    transact = read_xlsx_transactions(transactions_path)
    result = filter_transactions_by_current_month(transact, "12.03.2020")
    print(result)