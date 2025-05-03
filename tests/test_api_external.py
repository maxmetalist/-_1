
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_success_response
        mock_get.return_value = mock_response

        result = get_rate("USD", "RUB")
        assert result == {"RUB": 75.50}


def test_api_error(mock_error_response):

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

