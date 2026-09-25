import argparse
import re
from datetime import datetime, date

def is_valid_surname(surname : str) -> bool:
    """
    Проверка формата фамилии
    """
    return bool(re.fullmatch(r"[А-ЯЁ][а-яё]+", surname))

def parse_valid_date(date_string : str) -> date | None:
    """
    Преобразует строку с датой в объект date.

    Возвращает объект date, если дата существует и её год находится
    в диапазоне от 1900 до 2026 включительно. Иначе возвращает None.
    """
    if not date_string:
        return None
    try:
        normalized_date = re.sub(r'[/.-]', '-', date_string)
        date_obj = datetime.strptime(normalized_date, "%d-%m-%Y").date()

        if not date(1900,1,1) <= date_obj <= date.today():
            return None
        
        return date_obj
    except ValueError:
        return None

def find_surname(text : str) -> str | None:
    """
    Извлекает фамилию из текста анкеты.

    Ищет строку формата: "Фамилия: <значение>".
    Возвращает найденную фамилию или None,
    если такая строка отсутствует.
    """
    surname = ""
    pattern = r'Фамилия:\s*(\w+)'

    match = re.search(pattern, text)
    if match:
        surname = match.group(1)
        return surname
    else:
        return None

def find_date(text : str) -> str | None:
    """
    Извлекает строку с датой из текста анкеты.

    Поддерживает даты в форматах "день.месяц.год",
    "день-месяц-год", "день/месяц/год", где день и месяц
    могут состоять из одной или двух цифр, а год - из четырёх цифр.

    Возвращает найденную строку или None, если такая строка отсутствует.
    """
    date_string = ""
    pattern = r'\d{1,2}[/.-]\d{1,2}[/.-]\d{4}'

    match = re.search(pattern, text)
    if match:
        date_string = match.group(0)
        return date_string
    else:
        return None

def find_surnames_and_dates_of_birth(text : str) -> list[tuple[str, date]]:
    """
    Поиск корректных фамилий и дат рождения из списка анкет.

    Входные данные: строка с содержимым файла data.txt.
    Выходные данные: список кортежей вида: (фамилия, дата рождения).
    Дата рождения преобразуется в объект datetime.date
    """
    result = []
    parts = re.split(r'\n\s*\n', text)

    for i in parts:
        surname = find_surname(i)
        if not surname:
            continue

        date_string = find_date(i)
        if not date_string:
            continue

        if not is_valid_surname(surname):
            surname = surname.capitalize()

        birth_date = parse_valid_date(date_string)
        if birth_date is not None:
            result.append((surname, birth_date))

    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='путь к файлу с исходными анкетами')
    parser.add_argument('output_file', type=str, help='путь к файлу для сохранения результата')
    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding='utf-8') as file:
            text = file.read()
        

        res = find_surnames_and_dates_of_birth(text)
        res.sort(key=lambda x: x[1], reverse=True)

        with open(args.output_file, "w", encoding='utf-8') as file:
            for surname, birth_date in res:
                file.write(f"{surname}: {birth_date.strftime('%d.%m.%Y')}\n")
    except Exception as exc:
        print(f"Error: {exc}")

if __name__ == '__main__':
    main()