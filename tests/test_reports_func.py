import unittest
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from src.reports_func import filter_transactions_by_category


class TestFilterTransactionsByCategory(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        today = datetime.now().date()
        self.transactions = [
            {
                "Дата операции": f"{today.strftime('%d.%m.%Y')} 12:00:00",
                "Категория": "Фастфуд",
                "Сумма операции": "-200",
            },
            {
                "Дата операции": f"{(today - timedelta(days=30)).strftime('%d.%m.%Y')} 10:00:00",
                "Категория": "Фастфуд",
                "Сумма операции": "-150",
            },
            {
                "Дата операции": f"{(today - relativedelta(months=2)).strftime('%d.%m.%Y')} 15:00:00",
                "Категория": "Образование",
                "Сумма операции": "-500",
            },
            {
                "Дата операции": f"{(today - relativedelta(months=4)).strftime('%d.%m.%Y')} 09:00:00",
                "Категория": "Фастфуд",
                "Сумма операции": "-100",
            },
            {
                "Дата операции": "01.01.2020 14:00:00",
                "Категория": "Образование",
                "Сумма операции": "-300",
            },
            {"Категория": "Фастфуд"},
            {"Дата операции": "invalid_date"},
        ]

    def test_filter_by_category_current_date(self):
        """Тест фильтрации по категории с текущей датой"""
        result = filter_transactions_by_category(self.transactions, "Фастфуд")
        self.assertEqual(len(result), 2)

    def test_filter_by_category_with_custom_date(self):
        """Тест фильтрации с указанием даты вручную"""
        custom_date = "15.07.2023"
        result = filter_transactions_by_category(self.transactions, "Образование", date=custom_date)
        self.assertTrue(
            all(
                datetime.strptime(t["Дата операции"].split()[0], "%d.%m.%Y").date()
                <= datetime.strptime(custom_date, "%d.%m.%Y").date()
                for t in result
            )
        )

    def test_empty_result_for_nonexistent_category(self):
        """Тест пустого результата для несуществующей категории"""
        result = filter_transactions_by_category(self.transactions, "Несуществующая категория")
        self.assertEqual(len(result), 0)

    def test_handles_invalid_dates_gracefully(self):
        """Тест корректной обработки транзакций с некорректными датами"""
        result = filter_transactions_by_category(self.transactions, "Фастфуд")
        self.assertEqual(len(result), 2)

    def test_empty_input(self):
        """Тест пустого списка транзакций"""
        result = filter_transactions_by_category([], "Фастфуд")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
