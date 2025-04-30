import json
from functools import wraps
from typing import Any, Callable, Optional


def report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор для записи результатов функций-отчётов в файл"""

    def wrapper(func: Callable) -> Callable:

        @wraps(func)
        def decorator(*args: Any, **kwargs: Any) -> Any:
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
