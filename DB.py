import psycopg2
import local_settings as ls

def connect_to_database():
    return psycopg2.connect(
        dbname=ls.dbname,
        user=ls.user,
        password=ls.password,
        host=ls.host,
        port=ls.port
    )


def create_tables():
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # Создание таблицы Clients
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR UNIQUE NOT NULL
            )
            """)

        # Создание таблицы Client_phones
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Client_phones (
                id SERIAL PRIMARY KEY,
                client_id INT REFERENCES Clients(id),
                phone_number VARCHAR NOT NULL
            )
            """)

        conn.commit()
        print("Таблица создана")
    except psycopg2.Error as e:
        conn.rollback()
        print("Ошибка при создании таблицы:", e)
    finally:
        cur.close()
        conn.close()



def add_client(first_name, last_name, email):

    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # Добавление клиента
        cur.execute("""
        INSERT INTO Clients (first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id
        """, (first_name, last_name, email))

        client_id = cur.fetchone()[0]
        conn.commit()
        print("Клиент добавлен")
        return client_id
    except psycopg2.Error as e:
        conn.rollback()
        print("Ошибка при добавлении клиента:", e)
    finally:
        cur.close()
        conn.close()

def add_phone(client_id, phone_number):
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # Проверка заполнения поля ID
        if not client_id:
            raise Exception("Такого клиента не существует")

        # Добавление телефона
        cur.execute("""
        INSERT INTO Client_phones (client_id, phone_number)
        VALUES (%s, %s)
        """, (client_id, phone_number))

        conn.commit()
        print("Номер телефона успешно добавлен")
        return phone_number
    except psycopg2.Error as e:
        conn.rollback()
        print("Ошибка при добавлении номера", e)
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cur.close()
        conn.close()


def update_client(client_id, first_name='', last_name='', email='', phone_number=''):
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        # Проверка заполнения поля ID
        if not client_id:
            raise Exception("Такого клиента не существует")

        # Обновление данных клиента
        if first_name:
            cur.execute("""
            UPDATE Clients
            SET first_name = %s
            WHERE id = %s
            """, (first_name, client_id))

        if last_name:
            cur.execute("""
            UPDATE Clients
            SET last_name = %s
            WHERE id = %s
            """, (last_name, client_id))

        if email:
            cur.execute("""
            UPDATE Clients
            SET email = %s
            WHERE id = %s
            """, (email, client_id))

        if phone_number:
            # Проверка, существует ли уже телефон для данного клиента
            cur.execute("""
            SELECT client_id FROM Client_phones
            WHERE client_id = %s
            """, (client_id,))
            existing_phone = cur.fetchone()

            if existing_phone:
                # Если телефон уже существует, обновляем его
                cur.execute("""
                UPDATE Client_phones
                SET phone_number = %s
                WHERE client_id = %s
                """, (phone_number, client_id))
            else:
                # Если телефона еще нет, добавляем его
                cur.execute("""
                INSERT INTO Client_phones (client_id, phone_number)
                VALUES (%s, %s)
                """, (client_id, phone_number))

        conn.commit()
        print("Информация о клиенте изменена")

        return ()

    except psycopg2.Error as e:
        conn.rollback()
        print("Ошибка изменения информации о клиенте:", e)
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cur.close()
        conn.close()


def delete_phone(phone_number):
    try:

        conn = connect_to_database()
        cur = conn.cursor()

        # Удаление телефона
        cur.execute("""
            DELETE FROM client_phones
            WHERE phone_number = %s
        """, (phone_number,))

        conn.commit()

        print("Телефон успешно удален")
    except psycopg2.Error as e:
        print("Ошибка при удалении телефона:", e)
    finally:
        cur.close()
        conn.close()


def delete_client(client_id):
    try:

        conn = connect_to_database()
        cur = conn.cursor()

        # Удаление клиента
        cur.execute("""
            DELETE FROM clients
            WHERE id = %s
        """, (client_id,))

        conn.commit()

        print("Клиент успешно удален")
    except psycopg2.Error as e:
        print("Ошибка при удалении клиента:", e)
    finally:
        cur.close()
        conn.close()


def find_client(data):
    try:
        conn = connect_to_database()
        cur = conn.cursor()

        # Проверяем наличие данных для поиска
        if not data:
            Exception("Не указаны данные для поиска.")
            return None

        # Формируем условие поиска
        conditions = []
        parameters = []

        if 'first_name' in data:
            conditions.append("first_name ILIKE %s")
            parameters.append(f"%{data['first_name']}%")

        if 'last_name' in data:
            conditions.append("last_name ILIKE %s")
            parameters.append(f"%{data['last_name']}%")

        if 'email' in data:
            conditions.append("email ILIKE %s")
            parameters.append(f"%{data['email']}%")

        if 'phone_number' in data:
            conditions.append("Client_phones.phone_number ILIKE %s")
            parameters.append(f"%{data['phone_number']}%")

        if not conditions:
            print("Не указаны данные для поиска.")
            return None

        # Выполняем запрос на поиск клиентов
        query = f"SELECT clients.id, clients.first_name, clients.last_name, clients.email, Client_phones.phone_number FROM clients LEFT JOIN Client_phones ON clients.id = Client_phones.client_id WHERE {' AND '.join(conditions)}"
        cur.execute(query, tuple(parameters))
        clients = cur.fetchall()

        if clients:
            for client in clients:
                client_id, first_name, last_name, email, phone_number = client
                print(f"ID: {client_id}, First Name: {first_name}, Last Name: {last_name}, Email: {email}, Phone: {phone_number}")
            return clients
        else:
            print("Клиенты не найдены.")
            return None
    except psycopg2.Error as e:
        print("Ошибка при поиске клиента:", e)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

