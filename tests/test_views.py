

def test_normal_transactions():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "-200.75", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]

def test_failed_transactions():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "100.00", "Статус": "FAILED"},
        {"Номер карты": "1234", "Сумма платежа": "-200.00", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "300.00", "Статус": "FAILED"},
    ]

def test_negative_amounts():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "200.75", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]

def test_empty_card_number():
    transactions = [
        {"Номер карты": "", "Сумма платежа": "100.00", "Статус": "SUCCESS"},
        {"Номер карты": None, "Сумма платежа": "200.00", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-300.00", "Статус": "SUCCESS"},
    ]

def test_invalid_amounts():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "INVALID", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]

def test_empty_transactions():
    assert total_consume_card_number([]) == []


def test_get_top5_negative_transactions():
    test_data = [

    ]

    result = get_top5_transactions(test_data)

    assert len(result) == 5


def test_less_than_5_transactions():
    test_data = [

    ]

    result = get_top5_transactions(test_data)
    assert len(result) == 2


def test_empty_input():
