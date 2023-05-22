


# Проверка наличия существующего email
def search_email(cur, email):
    cur.execute("""
    SELECT id FROM clients WHERE email = %s
    """, (email,))
    existing_client = cur.fetchone()
    return existing_client



# Функция, создающая структуру БД (таблицы).
def create_tables(conn):
    cur = conn.cursor()

    # Таблица клиентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    # Таблица телефонов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            phone_number VARCHAR(20) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    print("Tables created successfully")


# Функция, позволяющая добавить нового клиента.
def add_client(conn, first_name, last_name, email):
    cur = conn.cursor()

    # Проверка наличия существующего email
    existing_client = search_email(cur, email)
    if existing_client:
        print("Client with the same email already exists")
        cur.close()
        return existing_client

    # Добавление клиента
    cur.execute("""
    INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (first_name, last_name, email))

    client_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    print("Client added successfully")

    return client_id


# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone_number):
    cur = conn.cursor()

    # Добавление телефона
    cur.execute("""
    INSERT INTO phones (client_id, phone_number)
        VALUES (%s, %s)
    """, (client_id, phone_number))

    conn.commit()
    cur.close()
    print("Phone added successfully")


# Функция, позволяющая изменить данные о клиенте.
def update_client(conn, client_id, first_name=None, last_name=None, email=None):
    cur = conn.cursor()

    # Изменение данных клиента
    if first_name:
        cur.execute("""
        UPDATE clients
            SET first_name = %s
            WHERE id = %s
        """, (first_name, client_id))

    if last_name:
        cur.execute("""
        UPDATE clients
            SET last_name = %s
            WHERE id = %s
        """, (last_name, client_id))

    if email:
        cur.execute("""
        UPDATE clients
            SET email = %s
            WHERE id = %s
        """, (email, client_id))

    conn.commit()
    cur.close()
    print("Client updated successfully")
    return client_id

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, phone_id):
    with conn.cursor() as cur:

        #Удаление телефона
        cur.execute("""
        DELETE FROM phones
            WHERE client_id IN (
                SELECT client_id
                FROM phones
                WHERE id = %s
            )
        """, (phone_id,))

        conn.commit()

        print("Phone deleted successfully")

# функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM clients 
            WHERE id = %s
        """, (client_id,))

        conn.commit()
    print("Client deleted successfully")

# функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, data):
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM clients 
            WHERE first_name ILIKE %s 
            OR last_name ILIKE %s 
            OR email ILIKE %s
        """, (f'%{data}%', f'%{data}%', f'%{data}%'))

    clients = cur.fetchall()
    if not clients:
        cur.execute("""
        SELECT * FROM phones 
            JOIN clients ON phones.client_id = clients.id 
            WHERE phone ILIKE %s
            """, (f'%{data}%',))
        clients = cur.fetchall()

    if clients:
        for client in clients:
            print(f"ID: {client[0]}, First Name: {client[1]}, Last Name: {client[2]}, Email: {client[3]}")
    else:
        print("No clients found")

    cur.close()
