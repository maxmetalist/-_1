

logger_utils = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "..\\logs\\", "utils.log"), mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s %(lineno)d")
file_handler.setFormatter(file_formatter)
logger_utils.addHandler(file_handler)
logger_utils.setLevel(logging.DEBUG)

from datetime import datetime
def filter_transactions_by_current_month(transactions, current_date=None):
    """Фильтрует транзакции с начала месяца по указанную дату"""
    if current_date is None:
        logger_utils.debug("Дата не задана, выбираем текущую дату")
        current_date = datetime.now()
    elif isinstance(current_date, str):
        logger_utils.debug("форматирование даты в формат дд.мм.гггг")
        current_date = datetime.strptime(current_date, '%d.%m.%Y')
    logger_utils.debug("Получение даты начала отчётного периода")
    first_day_of_month = current_date.replace(day=1)
    logger_utils.debug("Получение даты окончания отчётного периода")
    end_of_day = current_date.replace(hour=23, minute=59, second=59)

    filtered_transactions = []
    logger_utils.debug("Фильтрация транзакций по отчётному периоду")
    for transaction in transactions:
        try:
            op_date_str = transaction['Дата операции']
            op_date = datetime.strptime(op_date_str, '%d.%m.%Y %H:%M:%S')

            if first_day_of_month <= op_date <= end_of_day:
                filtered_transactions.append(transaction)
