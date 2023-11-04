from datetime import datetime


def Menu():
    print("Введите 1, если хотите создать заметку")
    print("Введите 2, если хотите вывести список заметок")
    key_count = getKeyCount()
    phone_dir = dict()
    while True:
        num = input("Введите Ваш выбор: ")
        print()
        if not num.isdigit():
            print("Вы ввели некорректное значение")
            break
        num = int(num)
        if num == 0:
            break
        elif num == 1:
            user = Input_User()
            # phone_dir, key_count = Create_User(phone_dir, key_count, user)
            Export_Data(user)
        elif num == 2:
            phone_dir = Import_Data(phone_dir)
            Print_Phone_Dir(phone_dir)
            break

        else:
            print("Вы ввели некорректное значение")
            print()
            break


def Input_User() -> list:
    user = []
    user.append(input("Введите заголовок заметки: "))
    user.append(input("Введите содержание заметки: "))
    user.append(datetime.now().date())
    print()
    return user


def Export_Data(user: list):
    file_name = getFileName()
    key_count = getKeyCount()
    if not FileExists(file_name):
        print(f"{file_name} не существует, но будет создан")

    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(f"{key_count};{user[0]};{user[1]};{user[2]}\n")
    print("Заметка сохранена успешно.")
    print()


def Import_Data(phone_dir_local: dict) -> dict:
    key_count = 1
    file_name = getFileName()
    with open(file_name, mode='rt', encoding='utf-8') as file:
        for line in file:
            _, heading, body, data = line.strip().split(';')
            phone_dir_local[key_count] = [heading, body, data]
            key_count += 1
    print("Операция чтения заметок выполнена успешно.")
    print()
    return phone_dir_local


def Print_Phone_Dir(phone_dir_local: dict):
    if not phone_dir_local:
        print("База данных не содержит ни одной заметки")
        return
    for key_count, user in phone_dir_local.items():
        print(f"Номер: {key_count}. Заголовок: {user[0]}. Дата: {user[2]}")
    print()


def FileExists(file_name: str):
    import os
    if os.path.exists(file_name):
        return True
    else:
        return False


def getFileName():
    import os.path as path1
    # from os.path import abspath
    MAIN_DIR = path1.abspath(path1.dirname(__file__))
    file_name = path1.join(MAIN_DIR, "noteDataBase.csv")
    return file_name


def getKeyCount():
    key_count = 1
    file_name = getFileName()
    if not FileExists(file_name):
        return key_count

    with open(file_name, mode='r', encoding='utf-8') as file:
        for line in file:
            key_count += 1
    return key_count


Menu()
