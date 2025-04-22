from unittest.mock import Mock, patch

import pytest

from src.api_external import get_rate, get_stocks_price


def test_successful_rate(mock_success_response):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_success_response
        mock_get.return_value = mock_response

        result = get_rate("USD", "RUB")
        assert result == {"RUB": 75.50}


def test_api_error(mock_error_response):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = mock_error_response
        mock_get.return_value = mock_response

        result = get_rate("EUR", "RUB")
        assert "Запрос отклонён. Причина: некорректные данные" in result


def test_invalid_currency_format():
    with pytest.raises(ValueError):
        get_rate("US", "RUB")

    with pytest.raises(ValueError):
        get_rate(123, "RUB")


@patch("src.api_external.requests.get")
def test_successful_response(mock_get):
    """Тест успешного ответа от API с корректными данными"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Meta Data": {"2. Symbol": "IBM"},
        "Time Series (60min)": {
            "2025-04-22 19:00:00": {"4. close": "243.7400"},
            "2025-04-22 18:00:00": {"4. close": "243.8100"},
        },
    }

    mock_get.return_value = mock_response

    result = get_stocks_price("IBM")
    assert result["symbol"] == "IBM"
    assert len(result["price"]) == 2
    assert result["price"]["2025-04-22 19:00:00"] == "243.7400"
    mock_get.assert_called_once()


@patch("src.api_external.requests.get")
def test_api_stock_error(mock_get):
    """Тест ошибки API (status_code != 200)"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response

    result = get_stocks_price("IBM")
    assert result == "Запрос отклонён. Укажите параметры запроса"


@patch("src.api_external.requests.get")
def test_invalid_symbol_type(mock_get):
    """Тест на некорректный тип символа (не строка)"""
    result = get_stocks_price(123)
    assert result == "Укажите символ требуемой котировки, например 'IBM'"
    mock_get.assert_not_called()


@patch("src.api_external.requests.get")
def test_empty_symbol(mock_get):
    """Тест на пустую строку символа"""
    result = get_stocks_price("   ")
    assert result == "Укажите символ требуемой котировки, например 'IBM'"
    mock_get.assert_not_called()
