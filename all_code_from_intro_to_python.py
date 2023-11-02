# 8.1[49]: Создать телефонный справочник с возможностью импорта и экспорта данных
# в формате csv. Доделать задание вебинара и реализовать Update, Delete
# Информация о человеке: Фамилия, Имя, Телефон, Описание

# Корректность и уникальность данных не обязательны.

# Функционал программы
# 1) телефонный справочник хранится в памяти в процессе выполнения кода.
# Выберите наиболее удобную структуру данных для хранения справочника.
# 2) CRUD: Create, Read, Update, Delete

# Create: Создание новой записи в справочнике: ввод всех полей новой записи,
# занесение ее в справочник.

# Read: он же Select. Выбор записей, удовлетворяющих заданном фильтру: по первой
# части фамилии человека. Берем первое совпадение по фамилии.

# Update: Изменение полей выбранной записи. Выбор записи, как и в Read, заполнение
#  новыми значениями.

# Delete: Удаление записи из справочника. Выбор - как в Read.

# 3) экспорт данных в текстовый файл формата csv
# 4) импорт данных из текстового файла формата csv
# Используйте функции для реализации значимых действий в программе
# (*) Усложнение.
# Сделать тесты для функций
# Разделить на model-view-controller

def Menu():
    print("Введите 1, если хотите ввести нового пользователя")
    print("Введите 2, если хотите найти и вывести информацию о пользователе на экран")
    print("Введите 3, если хотите изменить информацию о пользователе")
    print("Введите 4, если хотите удалить запись о пользователе")
    print("Введите 5, если хотите распечатать справочник")
    print("Введите 6, если хотите экспортировать справочник в файл формата .csv")
    print("Введите 7, если хотите импортировать данные в справочник из файла формата .csv")
    print("Нажмите 0 для выхода из меню и завершения работы программы")
    print()
    key_count = 0
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
            phone_dir, key_count = Create_User(phone_dir, key_count, user)
        elif num == 2:
            key_count = search_User(phone_dir)
        elif num == 3:
            phone_dir = Update_User(phone_dir)
        elif num == 4:
            Delete_User(phone_dir)
        elif num == 5:
            Print_Phone_Dir(phone_dir)
        elif num == 6:
            Export_Data(phone_dir)
        elif num == 7:
            phone_dir, key_count = Import_Data(phone_dir, key_count)
        else:
            print("Вы ввели некорректное значение")
            print()
            break


# 1
def Input_User() -> list:
    user = []
    user.append(input("Введите фамилию пользователя: "))
    user.append(input("Введите имя пользователя: "))
    user.append(input("Введите телефон пользователя: "))
    user.append(input("Введите описание: "))
    print()
    return user


# 1
def Create_User(phone_dir_local: dict, key_count: int, user: list) -> dict:
    key_count += 1
    phone_dir_local[key_count] = user
    return phone_dir_local, key_count


# 2
def search_User(phone_dir_local: dict) -> int:
    import sys
    input_data = str(input("Введите фамилию пользователя полностью или первые буквы фамилии: ")).lower().capitalize()
    for key_count_found, user in phone_dir_local.items():
        if user[0].startswith(input_data):
            print_confirmation = str(input("Распечатать найденный результат? Y/N: ")).capitalize()
            if print_confirmation == 'Y':
                print(phone_dir_local[key_count_found])
                return key_count_found
            else:
                return key_count_found
    else:
        print("Такого пользователя не существует. Выполнение программы будет приостановлено")
        print()
        sys.exit()


# 3
def Update_User(phone_dir_local: dict) -> dict:
    key_count_local = search_User(phone_dir_local)
    if key_count_local not in phone_dir_local.keys():
        return
    new_family_name = str(input("Введите новую фамилию пользователя: "))
    new_user_name = str(input("Введите новое имя пользователя: "))
    new_phone_number = str(input("Введите новый телефон пользователя: "))
    new_description = str(input("Введите новое описание пользователя: "))
    update_confirmation = str(input(
        "Подтвердите внесение изменений, нажав 'Y'. Нажмите 'N' для возврата в главное меню: ")).capitalize()
    if update_confirmation == 'Y':
        user = []
        user.append(new_family_name)
        user.append(new_user_name)
        user.append(new_phone_number)
        user.append(new_description)
        phone_dir_local[key_count_local] = user
        return phone_dir_local
    else:
        return phone_dir_local


# 4
def Delete_User(phone_dir_local: dict):
    key_count_local = search_User(phone_dir_local)
    del_confirmation = str(
        input("Подтвердите удаление пользователя, нажав 'Y'. Нажмите 'N' для возврата в главное меню: ")).capitalize()
    if del_confirmation == 'Y':
        phone_dir_local.pop(key_count_local)
    else:
        return


# 5
def Print_Phone_Dir(phone_dir_local: dict):
    if not phone_dir_local:
        print("Телефонный справочник пуст")
        return
    for key_count, user in phone_dir_local.items():
        print(f"{key_count}: {user[0]} {user[1]} {user[2]} {user[3]}")
    print()


# 6
def Export_Data(phone_dir_local: dict):
    import os.path as path1
    # from os.path import abspath
    MAIN_DIR = path1.abspath(path1.dirname(__file__))
    file_name = path1.join(MAIN_DIR, "export.csv")
    with open(file_name, mode='w', encoding='utf-8') as file:
        for key_count, user in phone_dir_local.items():
            file.write(f"{key_count},{user[0]},{user[1]},{user[2]},{user[3]}\n")
    print("Операция выполнена успешно.")
    print()


# 7
def Import_Data(phone_dir_local: dict, key_count: int) -> dict:
    import os.path as path1
    # from os.path import abspath
    MAIN_DIR = path1.abspath(path1.dirname(__file__))
    file_name2 = path1.join(MAIN_DIR, "import.csv")
    with open(file_name2, mode='rt', encoding='utf-8') as file:
        for line in file:
            key_count += 1
            _, family_name, name, phone, description = line.strip().split('#')
            phone_dir_local[key_count] = [family_name, name, phone, description]
    print("Операция выполнена успешно.")
    print()
    return phone_dir_local, key_count


Menu()
