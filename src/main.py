from src.utils import get_current_time_string


def main(date_time):
    if date_time in range(5,11):
        print("Доброе утро!")
    elif date_time in range(11,16):
        print("Добрый день")
    elif date_time in range(16, 22):
        print("Добрый вечер")
    else:
        print("Доброй ночи")


if __name__ == "__main__":
    time = int(get_current_time_string())
    print(main(time))
