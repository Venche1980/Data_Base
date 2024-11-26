import psycopg2


# Функция для создания структуры базы данных
def create_db(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
            DROP TABLE IF EXISTS phones;
        ''')
        cursor.execute('''
            DROP TABLE IF EXISTS clients;
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100) UNIQUE
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
                phone_number VARCHAR(20)
            );
        ''')
        conn.commit()


# Функция для добавления нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING client_id;
        ''', (first_name, last_name, email))
        client_id = cursor.fetchone()[0]
        if phones:
            for phone in phones:
                add_phone(conn, client_id, phone)
        conn.commit()
        return client_id


# Функция для добавления телефона существующему клиенту
def add_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute('''
            INSERT INTO phones (client_id, phone_number)
            VALUES (%s, %s);
        ''', (client_id, phone))
        conn.commit()


# Функция для изменения данных о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cursor:
        if first_name:
            cursor.execute('''
                UPDATE clients SET first_name = %s WHERE client_id = %s;
            ''', (first_name, client_id))
        if last_name:
            cursor.execute('''
                UPDATE clients SET last_name = %s WHERE client_id = %s;
            ''', (last_name, client_id))
        if email:
            cursor.execute('''
                UPDATE clients SET email = %s WHERE client_id = %s;
            ''', (email, client_id))
        if phones is not None:
            cursor.execute('''
                DELETE FROM phones WHERE client_id = %s;
            ''', (client_id,))
            for phone in phones:
                add_phone(conn, client_id, phone)
        conn.commit()


# Функция для удаления телефона клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute('''
            DELETE FROM phones WHERE client_id = %s AND phone_number = %s;
        ''', (client_id, phone))
        conn.commit()


# Функция для удаления клиента
def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute('''
            DELETE FROM clients WHERE client_id = %s;
        ''', (client_id,))
        conn.commit()


# Функция для поиска клиента по имени, фамилии, email или телефону
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cursor:
        query = '''
            SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone_number
            FROM clients c
            LEFT JOIN phones p ON c.client_id = p.client_id
            WHERE 1=1
        '''
        params = []
        if first_name:
            query += ' AND c.first_name = %s'
            params.append(first_name)
        if last_name:
            query += ' AND c.last_name = %s'
            params.append(last_name)
        if email:
            query += ' AND c.email = %s'
            params.append(email)
        if phone:
            query += ' AND p.phone_number = %s'
            params.append(phone)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        if not results:
            print("Нет такого клиента")
        else:
            unique_clients = {}
            for result in results:
                client_id = result[0]
                if client_id not in unique_clients:
                    unique_clients[client_id] = result[:4] + ([],)
                unique_clients[client_id][4].append(result[4])

            for client in unique_clients.values():
                print(client)


# Создание подключения и демонстрация работы функций
with psycopg2.connect(database="clients_db", user="postgres", password="123") as conn:
    # Создание базы данных
    create_db(conn)

    # Добавление клиентов
    client1_id = add_client(conn, "Иван", "Иванов", "ivan.ivanov@example.com", phones=["+1234567890", "+0987654321"])
    print(f"Добавлен клиент с ID: {client1_id}")

    client2_id = add_client(conn, "Мария", "Смирнова", "maria.smirnova@example.com", phones=["+1122334455"])
    print(f"Добавлен клиент с ID: {client2_id}")

    client3_id = add_client(conn, "Алексей", "Петров", "alexey.petrov@example.com")
    print(f"Добавлен клиент с ID: {client3_id}")

    client4_id = add_client(conn, "Ольга", "Кузнецова", "olga.kuznetsova@example.com", phones=["+1222333444"])
    print(f"Добавлен клиент с ID: {client4_id}")

    client5_id = add_client(conn, "Дмитрий", "Соколов", "dmitry.sokolov@example.com",
                            phones=["+1444555666", "+1777888999"])
    print(f"Добавлен клиент с ID: {client5_id}")

    # Изменение данных клиента
    change_client(conn, client1_id, first_name="Джон")

    # Поиск клиента по email
    print("Ищем клиента по  email:")
    find_client(conn, email="ivan.ivanov@example.com")

    # Удаление телефона клиента
    delete_phone(conn, client1_id, "+1234567890")

    # Поиск клиента по email после удаления одного номера телефона
    print("Ищем клиента по  email:")
    find_client(conn, email="ivan.ivanov@example.com")

    # Удаление клиента
    delete_client(conn, client1_id)

    # Поиск клиента по email после удаления клиента
    print("Ищем клиента по email:")
    find_client(conn, email="ivan.ivanov@example.com")
