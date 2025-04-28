from src.views import get_top5_transactions, total_consume_card_number


def test_normal_transactions():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "-200.75", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]
    expected = [{"1234": "-301.25"}, {"5678": "-50.0"}]
    assert total_consume_card_number(transactions) == expected


def test_failed_transactions():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "100.00", "Статус": "FAILED"},
        {"Номер карты": "1234", "Сумма платежа": "-200.00", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "300.00", "Статус": "FAILED"},
    ]
    expected = [{"1234": "-200.0"}, {"5678": "0.0"}]
    assert total_consume_card_number(transactions) == expected


def test_negative_amounts():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "200.75", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]
    expected = [{"1234": "-100.5"}, {"5678": "-50.0"}]
    assert total_consume_card_number(transactions) == expected


def test_empty_card_number():
    transactions = [
        {"Номер карты": "", "Сумма платежа": "100.00", "Статус": "SUCCESS"},
        {"Номер карты": None, "Сумма платежа": "200.00", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-300.00", "Статус": "SUCCESS"},
    ]
    expected = [{"5678": "-300.0"}]
    assert total_consume_card_number(transactions) == expected


def test_invalid_amounts():
    transactions = [
        {"Номер карты": "1234", "Сумма платежа": "-100.50", "Статус": "SUCCESS"},
        {"Номер карты": "1234", "Сумма платежа": "INVALID", "Статус": "SUCCESS"},
        {"Номер карты": "5678", "Сумма платежа": "-50.00", "Статус": "SUCCESS"},
    ]
    expected = [{"1234": "-100.5"}, {"5678": "-50.0"}]
    assert total_consume_card_number(transactions) == expected


def test_empty_transactions():
    assert total_consume_card_number([]) == []


def test_get_top5_negative_transactions():
    test_data = [
        {"Статус": "OK", "Сумма платежа": "-100", "Описание": "Транзакция 1"},
        {"Статус": "OK", "Сумма платежа": "-500", "Описание": "Транзакция 2"},
        {"Статус": "OK", "Сумма платежа": "-200", "Описание": "Транзакция 3"},
        {"Статус": "OK", "Сумма платежа": "-50", "Описание": "Транзакция 4"},
        {"Статус": "OK", "Сумма платежа": "-1000", "Описание": "Транзакция 5"},
        {"Статус": "OK", "Сумма платежа": "-300", "Описание": "Транзакция 6"},
        {"Статус": "FAILED", "Сумма платежа": "-400", "Описание": "Транзакция 7"},
        {"Статус": "OK", "Сумма платежа": "100", "Описание": "Транзакция 8"},
    ]

    result = get_top5_transactions(test_data)

    assert len(result) == 5

    amounts = [float(t["Сумма платежа"]) for t in result]
    assert amounts == [-1000, -500, -300, -200, -100]
    assert all(float(t["Сумма платежа"]) < 0 for t in result)
    assert all(t["Статус"] == "OK" for t in result)


def test_less_than_5_transactions():
    test_data = [
        {"Статус": "OK", "Сумма платежа": "-100", "Описание": "Транзакция 1"},
        {"Статус": "OK", "Сумма платежа": "-200", "Описание": "Транзакция 2"},
    ]

    result = get_top5_transactions(test_data)
    assert len(result) == 2


def test_empty_input():
    assert get_top5_transactions([]) == []
