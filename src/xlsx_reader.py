import os.path

import pandas as pd



    """Функция, считывающая файл excel по указанному пути"""
    transactions_list_xlsx = []
    if not os.path.exists(transactions_xlsx_path):
        print(f"Файл не найден: {transactions_xlsx_path}")


        print("Файл должен быть в формате .xlsx")

    try:
        data_frame = pd.read_excel(transactions_xlsx_path, dtype=str, engine="openpyxl")
        df = data_frame.fillna(value="")
        transactions_list_xlsx = df.to_dict(orient="records")
    except Exception as ex:
        print(f"Произошла ошибка {ex}")
    return transactions_list_xlsx
