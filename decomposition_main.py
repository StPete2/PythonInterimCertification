from datetime import datetime


def Menu():
    print("Введите 1, если хотите создать заметку")
    print("Введите 2, если хотите вывести список заметок")
    print("Введите 3 для поиска заметки по её номеру")
    print("Введите 4 для редактирования заметки по её номеру")
    key_count = 0
    # key_count = getKeyCount()
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
            Export_Data(user)
        elif num == 2:
            phone_dir = Import_Data(phone_dir)
            Print_Phone_Dir(phone_dir)
        elif num == 3:
            phone_dir = Import_Data(phone_dir)
            Print_Phone_Dir(phone_dir)
            key_count = search_User(phone_dir)
            if key_count == 20000:
                break
            print_Selected_Note(phone_dir, key_count)
        elif num == 4:  # editing a note
            if key_count != 0:
                if not asking_a_question():
                    key_count = search_User(phone_dir)
            else:
                phone_dir = Import_Data(phone_dir)
                key_count = search_User(phone_dir)
                if key_count == 10000:
                    break
            user = Update_User(phone_dir, key_count)
            if not user == phone_dir[key_count]:
                save_note_after_editing(user, key_count)

            print("заглушка")
            # edit a note

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
    file_name = getFileName()
    with open(file_name, mode='rt', encoding='utf-8') as file:
        for line in file:
            key_count, heading, body, data = line.strip().split(';')
            phone_dir_local[key_count] = [heading, body, data]
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


def search_User(phone_dir_local: dict) -> int:
    input_data = input("Введите номер заметки: ")
    print()
    if not input_data.isdigit():
        print("Вы ввели некорректное значение")
        return 20000

    for key_count_found, user in phone_dir_local.items():
        if input_data == key_count_found:
            return key_count_found
    else:
        print("Заметки с таким номером не существует.")
        print()
        return 10000


def asking_a_question() -> bool:
    reply = str(input("Вы хотите отредактировать только что выбранную заметку? Y/N: ")).capitalize()
    if reply == 'Y':
        return True
    else:
        return False


def Update_User(phone_dir_local: dict, key_count_local: int) -> list:
    new_heading = str(input("Введите новое название заметки: "))
    new_body = str(input("Введите новое содержание заметки: "))
    new_data = datetime.now().date()
    update_confirmation = str(input(
        "Подтвердите внесение изменений, нажав 'Y'. Нажмите 'N' для возврата в главное меню: ")).capitalize()
    if update_confirmation == 'Y':
        user = []
        user.append(new_heading)
        user.append(new_body)
        user.append(new_data)
        # phone_dir_local[key_count_local] = user
        # print(user + "заглушка")
        return user
        # return phone_dir_local
    else:
        return phone_dir_local[key_count_local]
        # return phone_dir_local


def save_note_after_editing(user: list, key_count_local: int):
    file_name = getFileName()
    # if not FileExists(file_name):
    #     print(f"{file_name} не существует, но будет создан")

    with open(file_name, mode='r+', encoding='utf-8') as file:
        lines = file.readlines()
        a = int(key_count_local)-1
        lines[a] = f"{key_count_local};{user[0]};{user[1]};{user[2]}\n"
        # file.seek(0)
        file.writelines(lines)
        # for line in file.readlines():
        #     print(line)
        #     key_count, _, _, _ = line.strip().split(';')
        #     if key_count == key_count_local:
        #         # phone_dir_local[key_count]
        #         # with open(file_name, mode='w', encoding='utf-8') as file:
        #         file.write(f"{key_count_local};{user[0]};{user[1]};{user[2]}\n")
    print("Заметка сохранена успешно.")
    print()


def print_Selected_Note(phone_dir_local: dict, input_data: int):
    for key_count_found, user in phone_dir_local.items():
        if input_data == key_count_found:
            print(f"Заметка №{key_count_found}. Заголовок: {user[0]}. Дата: {user[2]}")
            print(f"Содержание заметки:")
            print(f"{user[1]}")


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
