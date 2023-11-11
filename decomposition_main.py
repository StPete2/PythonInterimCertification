from datetime import datetime


def Menu():
    print("Введите 1, если хотите создать заметку")
    print("Введите 2, если хотите вывести список заметок")
    print("Введите 3 для поиска заметки по её номеру и выводу содержания заметки")
    print("Введите 4 для редактирования заметки по её номеру")
    print("Введите 5 для удаления заметки по номеру")
    print("Введите 6")
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
            user = input_note()
            save_one_note(user)
        elif num == 2:
            phone_dir = import_all_notes(phone_dir)
            print_all_notes(phone_dir)
        elif num == 3:
            phone_dir = import_all_notes(phone_dir)
            # Print_Phone_Dir(phone_dir)
            key_count = search_note(phone_dir)
            if key_count == 20000:
                break
            print_selected_note(phone_dir, key_count)
        elif num == 4:  # editing a note
            if key_count != 0:
                if not asking_a_question("отредактировать"):
                    key_count = search_note(phone_dir)
            else:
                phone_dir = import_all_notes(phone_dir)
                key_count = search_note(phone_dir)
                if key_count == 10000:
                    break
            phone_dir = update_note(phone_dir, key_count)
            save_all_notes(phone_dir)

        elif num == 5:  # delete a note
            phone_dir = import_all_notes(phone_dir)
            key_count = search_note(phone_dir)
            if key_count == 10000:
                break
            delete_note(phone_dir, key_count)
            renumber_keys(phone_dir, key_count)
            save_all_notes(phone_dir)
        elif num == 6:
            a = getKeyCount2()
            print(a)

        else:
            print("Вы ввели некорректное значение")
            print()
            break


def input_note() -> list:
    user = []
    user.append(input("Введите заголовок заметки: "))
    user.append(input("Введите содержание заметки: "))
    user.append(datetime.now().date())
    print()
    return user


def save_one_note(user: list):
    file_name = getFileName()
    key_count = getKeyCount()
    if not FileExists(file_name):
        print(f"{file_name} не существует, но будет создан")

    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(f"{key_count};{user[0]};{user[1]};{user[2]}\n")
    print("Заметка сохранена успешно.")
    print()


def import_all_notes(phone_dir_local: dict) -> dict:
    file_name = getFileName()
    with open(file_name, mode='rt', encoding='utf-8') as file:
        for line in file:
            key_count, heading, body, data = line.strip().split(';')
            key_count = int(key_count)
            phone_dir_local[key_count] = [heading, body, data]
    print("Операция чтения заметок выполнена успешно.")
    print()
    return phone_dir_local


def print_all_notes(phone_dir_local: dict):
    if not phone_dir_local:
        print("База данных не содержит ни одной заметки")
        return
    for key_count, user in phone_dir_local.items():
        print(f"Номер: {key_count}. Заголовок: {user[0]}. Дата: {user[2]}")
    print()


def save_all_notes(phone_dir_local: dict):
    file_name = getFileName()
    with open(file_name, mode='w', encoding='utf-8') as file:
        print()
        # file.write()

    with open(file_name, mode='w', encoding='utf-8') as file:
        for key_count, user in phone_dir_local.items():
            file.write(f"{key_count};{user[0]};{user[1]};{user[2]}\n")
    print()


def search_note(phone_dir_local: dict) -> int:
    input_data = input("Введите номер заметки: ")
    if not input_data.isdigit():
        print("Вы ввели некорректное значение")
        return 20000
    print()
    input_data = int(input_data)
    for key_count_found, user in phone_dir_local.items():
        if input_data == key_count_found:
            return key_count_found
    else:
        print("Заметки с таким номером не существует.")
        print()
        return 10000


def asking_a_question(text: str) -> bool:
    reply = str(input(f"Вы хотите {text} только что выбранную заметку? Y/N: ")).capitalize()
    if reply == 'Y':
        return True
    else:
        return False


def update_note(phone_dir_local: dict, key_count_local: int) -> dict:
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
        phone_dir_local[key_count_local] = user
        return phone_dir_local
    else:
        return phone_dir_local


def delete_note(phone_dir_local: dict, key_count_local: int) -> dict:
    del_confirmation = str(
        input("Подтвердите удаление пользователя, нажав 'Y'. Нажмите 'N' для возврата в главное меню: ")).capitalize()
    if del_confirmation == 'Y':
        phone_dir_local.pop(key_count_local)
        return phone_dir_local
    else:
        return phone_dir_local


def renumber_keys(phone_dir_local: dict, key_count_local: int) -> dict:
    total_number_notes = getKeyCount()
    if total_number_notes == key_count_local-1:  # to delete a last note
        return phone_dir_local
    elif key_count_local == total_number_notes:
        phone_dir_local[total_number_notes] = phone_dir_local[total_number_notes+1]
        phone_dir_local.pop(total_number_notes+1)
        return phone_dir_local
    elif key_count_local != total_number_notes:
        for i in range(0, total_number_notes-key_count_local-1):
            heading, note, data = phone_dir_local.get(i + key_count_local + 1)
            user = [heading, note, data]
            phone_dir_local[i + key_count_local] = user
            print(f"key = {i+key_count_local}; {phone_dir_local.get(i+key_count_local)}")
            phone_dir_local.pop(i+key_count_local+1)
        return phone_dir_local


def print_selected_note(phone_dir_local: dict, input_data: int):
    for key_count_found, user in phone_dir_local.items():
        if input_data == key_count_found:
            print(f"Заметка №{key_count_found}. Заголовок: {user[0]}. Дата: {user[2]}")
            print(f"Содержание заметки: {user[1]}\n")


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


def getKeyCount() -> int:
    key_count = 1
    file_name = getFileName()
    if not FileExists(file_name):
        return key_count

    with open(file_name, mode='r', encoding='utf-8') as file:
        for line in file:
            key_count += 1
    return key_count


def getKeyCount2() -> int:
    key_count = 1
    file_name = getFileName()
    if not FileExists(file_name):
        return key_count
    with open(file_name, mode='r', encoding='utf-8') as file:
        key_count, _, _, _ = file.readlines()[-1].split(";")
        key_count = int(key_count)
    return key_count


Menu()
