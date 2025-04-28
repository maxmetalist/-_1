import re
import unittest

from src.servises import filter_person_transfer, find_transactions_by_name


class TestFilterPersonTransfer(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_transactions = [
            {
                "Дата операции": "15.01.2023 12:00:00",
                "Категория": "Переводы",
                "Описание": "Иван П.",
                "Сумма операции": "-1000",
                "Валюта операции": "RUB",
            },
            {
                "Дата операции": "16.01.2023 13:00:00",
                "Категория": "Магазины",
                "Описание": "Петр С.",
                "Сумма операции": "-500",
                "Валюта операции": "RUB",
            },
            {
                "Дата операции": "17.01.2023 14:00:00",
                "Категория": "Переводы",
                "Описание": "Перевод в банк",
                "Сумма операции": "-2000",
                "Валюта операции": "RUB",
            },
            {
                "Дата операции": "18.01.2023 15:00:00",
                "Категория": "Переводы",
                "Описание": "Мария В.",
                "Сумма операции": "-1500",
                "Валюта операции": "RUB",
            },
            {
                "Дата операции": "19.01.2023 16:00:00",
                "Категория": "Переводы",
                "Описание": "Алексей Б.",
                "Сумма операции": "-3000",
                "Валюта операции": "RUB",
            },
        ]

    def test_finds_person_transfers(self):
        """Тест нахождения переводов физ лицам"""
        result = filter_person_transfer(self.test_transactions)
        self.assertEqual(len(result), 3)

    def test_returned_fields(self):
        """Тест правильности возвращаемых полей"""
        result = filter_person_transfer(self.test_transactions)
        expected_fields = {"Дата операции", "Сумма операции", "Валюта операции", "Описание"}

        for transaction in result:
            self.assertEqual(set(transaction.keys()), expected_fields)

    def test_name_pattern_matching(self):
        """Тест соответствия шаблону имени"""
        result = filter_person_transfer(self.test_transactions)
        name_pattern = re.compile(r"[А-ЯЁа-яё]+\s[А-ЯЁ]\.")

        for transaction in result:
            self.assertIsNotNone(name_pattern.search(transaction["Описание"]))

    def test_empty_input(self):
        """Тест с пустым списком транзакций"""
        result = filter_person_transfer([])
        self.assertEqual(result, [])

    def test_no_matching_transactions(self):
        """Тест, когда нет подходящих транзакций"""
        no_matching = [
            {
                "Дата операции": "20.01.2023 17:00:00",
                "Категория": "Магазины",
                "Описание": "Покупка в магазине",
                "Сумма операции": "-100",
                "Валюта операции": "RUB",
            }
        ]
        result = filter_person_transfer(no_matching)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()


class TestTransactionFunctions(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.sample_transactions = [
            {
                "Дата операции": "01.01.2023 12:00",
                "Категория": "Переводы",
                "Описание": "Иван П.",
                "Сумма операции": "-500",
                "Валюта операции": "RUB",
                "Сумма платежа": "-500",
            },
            {
                "Дата операции": "02.01.2023 13:00",
                "Категория": "Переводы",
                "Описание": "Мария С.",
                "Сумма операции": "-1000",
                "Валюта операции": "RUB",
                "Сумма платежа": "-1000",
            },
            {
                "Дата операции": "03.01.2023 14:00",
                "Категория": "Магазины",
                "Описание": "Покупка продуктов",
                "Сумма операции": "-200",
                "Валюта операции": "RUB",
                "Сумма платежа": "-200",
            },
            {
                "Дата операции": "04.01.2023 15:00",
                "Категория": "Переводы",
                "Описание": "ООО Рога и копыта",
                "Сумма операции": "-5000",
                "Валюта операции": "RUB",
                "Сумма платежа": "-5000",
            },
        ]

    def test_find_transactions_by_name_exact_match(self):
        """Тест точного совпадения имени"""
        result = find_transactions_by_name(self.sample_transactions, "Иван")
        self.assertEqual(len(result), 1)
        self.assertIn("01.01.2023 12:00", result)
        self.assertEqual(result["01.01.2023 12:00"], "-500")

    def test_find_transactions_by_name_no_match(self):
        """Тест отсутствия совпадений"""
        result = find_transactions_by_name(self.sample_transactions, "Петр В.")
        self.assertEqual(len(result), 0)

    def test_find_transactions_by_name_empty(self):
        """Тест с пустым входом"""
        self.assertEqual(find_transactions_by_name([], "Иван П."), {})


if __name__ == "__main__":
    unittest.main()
