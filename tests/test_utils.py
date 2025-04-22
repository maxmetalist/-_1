import pytest

from unittest.mock import patch
import datetime

from src.utils import get_current_time_string, filter_transactions_by_current_month


def test_filter_and_sort():
    test_data = [
        {'Дата операции': '15.01.2023 12:00:00', 'Сумма': '200'},
        {'Дата операции': '01.01.2023 10:00:00', 'Сумма': '100'},
        {'Дата операции': '31.01.2023 23:59:59', 'Сумма': '300'},
    ]

    result = filter_transactions_by_current_month(test_data, "31.01.2023")

    assert [t['Сумма'] for t in result] == ['100', '200', '300']
    assert len(result) == 3


def test_edge_cases():
    test_data = [
        {'Дата операции': '01.01.2023 00:00:00', 'Сумма': '100'},
        {'Дата операции': '31.01.2023 23:59:59', 'Сумма': '200'},
        {'Дата операции': '01.02.2023 00:00:00', 'Сумма': '300'},
    ]

    result = filter_transactions_by_current_month(test_data, "31.01.2023")
    assert len(result) == 2
    assert result[0]['Сумма'] == '100'
    assert result[1]['Сумма'] == '200'
