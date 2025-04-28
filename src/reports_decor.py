import json
import os
from functools import wraps

from src.reports_func import filter_transactions_by_category
from src.xlsx_reader import read_xlsx_transactions


def report_to_file(filename=None):
    """Декоратор для записи результатов функций-отчётов в файл"""

    def wrapper(func):

        @wraps(func)
        def decorator(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename:
                report_filename = filename
                with open(report_filename, "a", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                print(f"Отчёт сохранён в файле {report_filename}")
            else:
                print("Укажите имя файла для записи отчёта")
            return result

        return decorator

    return wrapper


@report_to_file(os.path.join(os.path.dirname(__file__), "..\\data\\", "reports"))
def my_func():
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "operations.xlsx")
    transact = read_xlsx_transactions(transactions_path)
    res = filter_transactions_by_category(transact, "Переводы", "20.03.2020")
    return res


my_func()
