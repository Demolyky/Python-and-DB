import DB as db


def search_null(text):
    string = input(text)
    if string == '':
        return None
    else:
        return string

def main():
    # Создание таблиц
    db.create_tables()

    while True:
        command = input('Введите команду("помощь - список команд"):')
        match command.lower():
            case 'помощь':
                print("""
                "помощь" - список команд,
                "добавить клиента" - добавить клиента,
                "добавить телефон" - добавить телефон,
                "изменить" - изменить контакт или номер телефона,
                "удалить клиента" - удалить клиента,
                "удалить телефон" - удалить номер телефона,
                "поиск" - искать в базе,
                "выход" - выход
                """)

            case "добавить клиента":
                client_id = db.add_client(search_null('Введите имя: '), search_null('Введите фамилию: '), search_null('Введите электронную почту: '))
                print('ID нового клиента: ', client_id)
            case "добавить телефон":
                phone_number = db.add_phone(search_null('Введите ID пользователя: '), search_null('Введите номер телефона: '))
                print(f'Телефонный номер {phone_number} добавлен')
            case "изменить":
                db.update_client(
                    search_null('Введите ID пользователя: '),
                    search_null('Введите новое имя(оставьте пустое поле, чтобы не изменять): '),
                    search_null('Введите новую фамилию(оставьте пустое поле, чтобы не изменять): '),
                    search_null('Введите новую эл. почту(оставьте пустое поле, чтобы не изменять): '),
                    search_null('Введите новый номер телефона(оставьте пустое поле, чтобы не изменять): ')
                )
            case "удалить телефон":
                db.delete_phone(search_null('Введите номер телефона, который требуется удалить: '))
            case "удалить клиента":
                db.delete_client(search_null('Введите ID клиента для удаления: '))
            case "поиск":
                data = {}
                def find_null(row, text):
                    return {row: text} if text else {}

                data.update(find_null('first_name', search_null('Введите имя: ')))
                data.update(find_null('last_name', search_null('Введите фамилию: ')))
                data.update(find_null('email', search_null('Введите  эл. почту: ')))
                data.update(find_null('phone_number', search_null('Введите  номер телефона: ')))
                db.find_client(data)
            case "выход":
                print("Работа с БД завершена")
                break


if __name__ == '__main__':
    main()
