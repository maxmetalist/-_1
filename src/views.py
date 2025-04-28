import logging
import os

logger_views_card = logging.getLogger("views")
file_handler_card = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "views_card.log"), mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s %(lineno)d")
file_handler_card.setFormatter(file_formatter)
logger_views_card.addHandler(file_handler_card)
logger_views_card.setLevel(logging.DEBUG)


def total_consume_card_number(transact):
    """Функция подсчёта общего количества расходов по номерам карт(учитываются только платежи со статусом OK)"""
    card_dict = {}
    for transaction in transact:
        logger_views_card.debug("Проверка содержимого ячейки номера карты")
        card_number = transaction.get("Номер карты")
        amount_str = transaction.get("Сумма платежа")
        state = transaction.get("Статус")

        if not card_number:
            continue
        try:
            amount = float(amount_str)
        except ValueError:
            continue
        logger_views_card.debug("Проверка вхождения номера карты")
        if card_number not in card_dict.keys():
            card_dict[card_number] = 0.0
        logger_views_card.debug("Проверка на статус и отрицательность суммы")
        if state != "FAILED" and "-" in transaction.get("Сумма платежа"):
            card_dict[card_number] += amount
    logger_views_card.debug("Переформатирование полученных числовых значений в строковый формат")
    result = []
    for card_number, total in card_dict.items():
        result.append({card_number: str(round(total, 2))})

    return result


logger_views_top5 = logging.getLogger("views")
file_handler_top5 = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "views_top5.log"), mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s %(lineno)d")
file_handler_top5.setFormatter(file_formatter)
logger_views_top5.addHandler(file_handler_top5)
logger_views_top5.setLevel(logging.DEBUG)


def get_top5_transactions(transact):
    """Возвращает 5 самых больших по модулю отрицательных транзакций со статусом OK"""
    logger_views_top5.debug("Фильтруем транзакции: только статус OK и отрицательная сумма платежа")
    filtered = [
        transaction
        for transaction in transact
        if transaction.get("Статус") == "OK" and float(transaction.get("Сумма платежа", "0")) < 0
    ]
    logger_views_top5.debug("Сортировка по убыванию")
    sorted_trans = sorted(filtered, key=lambda x: float(x["Сумма платежа"]))

    return sorted_trans[:5]
