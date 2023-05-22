import psycopg2
import DB as db

conn = psycopg2.connect(
    dbname="Clients-Server",
    user="",
    password="",
    host="localhost",
    port="5432"
)

def main():
    # создание таблиц
    # db.create_tables(conn)

    # добавление клиента
    client_id = db.add_client(conn, "John", "Doe", "johndoe@example.com")

    # добавление телефона для клиента
    phone_id = db.add_phone(conn, client_id, "123456780")

    # изменение данных клиента
    # client_id = db.update_client(conn, client_id, "Jane", "Doe", "janedoe@example.com")

    # удаление телефона для клиента
    db.delete_phone(conn, phone_id)

    # удаление клиента
    db.delete_client(conn, client_id)

    # поиск клиентов
    search_results = db.find_client(conn, "Jane")
    print(search_results)


if __name__ == '__main__':
    main()
