import os
from unittest.mock import patch

import pandas as pd

from src.xlsx_reader import read_xlsx_transactions


def test_read_xlsx_transactions_wrong_path():
    transactions_xlsx_path = os.path.join("transactions_excel.xlsx")
    result = read_xlsx_transactions(transactions_xlsx_path)
    assert result == []


@patch("pandas.read_excel")
def test_read_xlsx_transactions_correct(mock_read_excel):
    """Тест на нормальную работу функции с подменой данных"""
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "transactions_excel.xlsx")
    mock_data = pd.DataFrame({"id": ["1", "2", "3"], "state": ["a", "b", "c"], "currency_name": ["d", "e", "f"]})
    mock_read_excel.return_value = mock_data
    result = read_xlsx_transactions(transactions_path)
    exp = [
        {"id": "1", "state": "a", "currency_name": "d"},
        {"id": "2", "state": "b", "currency_name": "e"},
        {"id": "3", "state": "c", "currency_name": "f"},
    ]
    assert result == exp


@patch("pandas.read_excel")
def test_read_xlsx_transactions_no_file(mock_read_excel):
    transactions_path = os.path.join(os.path.dirname(__file__), "..\\data\\", "transactions_excel.xlsx")
    mock_data = pd.DataFrame()
    mock_read_excel.return_value = mock_data
    result = read_xlsx_transactions(transactions_path)
    exp = []
    assert result == exp
