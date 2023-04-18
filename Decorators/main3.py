from pprint import pprint
from datetime import datetime
import re

## Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("Reg_exp/phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)


# Функция декоратор
def logger(old_function):
    start_time = datetime.now()

    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open("main.log", "a", encoding="utf-8") as f:
            i = f.write(str(start_time) + "\n")
            a = f.write(str(result) + "\n")
            b = f.write(old_function.__name__ + "\n")
            if args != ():
                c = f.write(str(args) + "\n")
            if kwargs != {}:
                d = f.write(str(kwargs) + "\n")

        return result

    end_time = datetime.now()
    return new_function


# Функция проверка на совпадения и получения индекса.
@logger
def get_index(lastname, corrected):
    for index, value in enumerate(corrected):
        if lastname == value[0]:
            return index


corrected_list = []
for i in contacts_list:
    pattern = r"\w+"
    name = re.findall(pattern, i[0])

    match len(name):
        case 3:
            i[2] = name[2]
            i[1] = name[1]
            i[0] = name[0]
        case 2:
            i[1] = name[1]
            i[0] = name[0]
    name = re.findall(pattern, i[1])
    if len(name) == 2:
        i[1] = name[0]
        i[2] = name[1]

    # Проверкаи замена телефона.
    i[5] = re.sub(
        r"(\+7|8) ?\(?(\d{3})\)?[ -]?(\d{3})-?(\d{2})-?(\d{2})(?:[ (]*(доб\.)? (\d{4})\)?)?",
        r"+7(\2)\3-\4-\5 \6\7",
        i[5],
    ).strip()

    if index := get_index(i[0], corrected_list):
        for t in range(len(corrected_list[index])):
            if not corrected_list[index][t]:
                corrected_list[index][t] = i[t]
    else:
        corrected_list.append(i)


if __name__ == "__main__":
    with open("Reg_exp/phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=",")
        datawriter.writerows(corrected_list)

    print(corrected_list)
