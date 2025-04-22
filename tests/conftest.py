import pytest


@pytest.fixture
def mock_success_response():
    return {
        "rates": {"RUB": 75.50},
        "base": "USD",
        "success": True
    }


@pytest.fixture
def mock_error_response():
    return {
        "error": {
            "code": "invalid_base_currency",
            "message": "Invalid base currency"
        }
    }