import json
import os

from src.reports_decor import report_to_file


def sample_report_function():
    return {"data": "тестовые данные", "status": "ok"}


def test_report_to_file_with_filename(tmp_path):
    """Проверяем запись отчёта в файл, если указано имя файла"""
    test_filename = tmp_path / "test_report.json"

    decorated_func = report_to_file(filename=str(test_filename))(sample_report_function)
    result = decorated_func()

    assert result == {"data": "тестовые данные", "status": "ok"}

    assert os.path.exists(test_filename)
    with open(test_filename, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == {"data": "тестовые данные", "status": "ok"}


def test_report_to_file_without_filename(capsys):
    """Проверяем поведение декоратора, если имя файла не указано"""
    decorated_func = report_to_file()(sample_report_function)
    result = decorated_func()

    assert result == {"data": "тестовые данные", "status": "ok"}

    captured = capsys.readouterr()
    assert "Укажите имя файла для записи отчёта" in captured.out


def test_report_to_file_appending_to_file(tmp_path):
    """Проверяем, что декоратор дописывает данные в файл, а не перезаписывает"""
    test_filename = tmp_path / "test_report_append.json"

    decorated_func = report_to_file(filename=str(test_filename))(sample_report_function)
    decorated_func()

    another_report = lambda: {"new_data": "доп данные"}
    decorated_another = report_to_file(filename=str(test_filename))(another_report)
    decorated_another()

    with open(test_filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert '"data": "тестовые данные"' in content
    assert '"new_data": "доп данные"' in content


def test_report_to_file_preserves_function_metadata():
    """Проверяем, что декоратор сохраняет метаданные оригинальной функции"""

    @report_to_file(filename="dummy.json")
    def test_func():
        """Тестовая функция"""
        return {}

    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Тестовая функция"
