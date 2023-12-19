import psycopg2


def create_delete_db(name, command, if_):
    conn_ = psycopg2.connect(database='postgres', user='postgres', password='6056')
    conn_.autocommit = True
    with conn_.cursor() as cur:
        sql = f"""{command} DATABASE {if_} {name}"""
        print(sql)
        cur.execute(sql)
    conn_.close()


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients(
                        client_id    SERIAL
                        PRIMARY KEY,
                        first_name   VARCHAR(100)       NOT NULL,
                        last_name    VARCHAR(100)       NOT NULL,
                        email        VARCHAR(80) UNIQUE NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS phones(
                        phone_id     SERIAL
                        PRIMARY KEY,
                        phone        VARCHAR(11) UNIQUE NULL,
                        client_id    INTEGER        NOT NULL,
                                     CONSTRAINT fk_client
                        FOREIGN KEY(client_id)
                                     REFERENCES clients(client_id) ON DELETE CASCADE
                    );
                    """)
        print('структура БД создана')


def add_client(conn):
    first_name = input('Введите имя: ')
    last_name = input('Введите фамилию: ')
    email = input('Введите email: ')
    if first_name not in '' and last_name not in '' and email not in '':
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO clients (first_name, last_name, email)
                        VALUES (%s, %s, %s);
                        """, (first_name, last_name, email))
            conn.commit()
            print(f'Запись создана\n'
                  f'Имя {first_name} записан\n'
                  f'Фамилия {last_name} записан\n'
                  f'email {email} записан')
            add_phone(conn, email)
    else:
        print('ОТМЕНА: вводимые данные не должны быть пустыми!')


def add_phone(conn, email):
    phone = input('Введите номер телефона до 11 чисел: ')
    client_id = search_id(conn, email)
    with conn.cursor() as cur:
        if is_number(phone):
            cur.execute("""
                        INSERT INTO phones (phone, client_id)
                        VALUES (%s, %s);
                        """, (phone, client_id))
            print(f'номер телефона {phone} записан')
        else:
            print('номер телефона не записан')
        conn.commit()


def menu_update_db(conn_, email):
    n = input('* 1 - email\n'
              '* 2 - Имя\n'
              '* 3 - Фамилия\n'
              '* 4 - Номер телефона\n'
              'Какие данные изменить? Введите число: ')

    client_id = search_id(conn_, email)

    while True:
        if n == '1':
            new_email = input('Введите новый email: ')
            update_db(conn_, new_email, 'email',
                      'clients', client_id, 'client_id')
            break
        elif n == '2':
            new_first_name = input('Введите новое имя: ')
            update_db(conn_, new_first_name, 'first_name',
                      'clients', client_id, 'client_id')
            break
        elif n == '3':
            new_last_name = input('Введите новую фамилию: ')
            update_db(conn_, new_last_name, 'last_name',
                      'clients', client_id, 'client_id')
            break
        elif n == '4':
            update_phone(conn_, client_id)
            break
        else:
            print('ОТМЕНА: ничего не выбрано')
            break


def update_db(conn_, new_data, data_type, table_name, line, attribute_name):

    with conn_.cursor() as cur:
        cur.execute(f"""
                    UPDATE {table_name}
                       SET {data_type} = %s
                     WHERE {attribute_name} = %s;
                    """, (new_data, line))
        print(f'Данные в {data_type} изменены на {new_data}')


def update_phone(conn_, client_id):
    phones_dict = client_phones(conn_, client_id)
    key_ = phone_info(conn_, client_id)

    if is_number(key_) and len(phones_dict) >= int(key_) > 0:
        new_phone = input('Введите новый номер телефона до 11 чисел: ')
        update_db(conn_, new_phone, 'phone',
                  'phones', phones_dict[int(key_)], 'phone')
    else:
        print('ОТМЕНА: выбранный ключ не соответствует ни одному номеру телефона')


def delete_phone(conn_, email):
    client_id = search_id(conn_, email)
    phones_dict = client_phones(conn_, client_id)
    key_ = phone_info(conn_, client_id)
    phone = phones_dict[int(key_)]
    with conn_.cursor() as cur:
        cur.execute("""
                    SELECT phone_id
                      FROM phones
                     WHERE phone = %s
                    """, (phone,))

        phone_id = cur.fetchone()[0]

        cur.execute("""
                    DELETE FROM phones 
                    WHERE phone_id = %s;
                    """, (phone_id,))
        print(f'номер телефона {phone} удален')


def delete_client(conn_, email):
    client_id = search_id(conn_, email)
    with conn_.cursor() as cur:
        cur.execute("""
                    DELETE FROM clients 
                     WHERE client_id = %s;
                    """, (client_id,))
    print(f'все записи о клиенте {email} удалены')


def search_client(conn):
    sample_dict = {
        1: 'first_name',
        2: 'last_name',
        3: 'email',
        4: 'phone'
    }
    print('********************')
    key_ = input('Найти по:\n'
                 '* Имени    - ключ 1\n'
                 '* Фамилии  - ключ 2\n'
                 '* email    - ключ 3\n'
                 '* Телефону - ключ 4\n'
                 'Выберите номер ключа: ')
    with conn.cursor() as cur:
        if key_ == '1' or key_ == '2' or key_ == '3':
            attribute_name = sample_dict[int(key_)]
            client_data = input(f'Введите его {attribute_name}: ')
            result_search_client(cur, attribute_name, client_data)
        elif key_ == '4':
            attribute_name = sample_dict[int(key_)]
            client_data = input(f'Введите его {attribute_name}: ')
            cur.execute(f"""
                        SELECT client_id
                          FROM phones
                         WHERE {attribute_name} = %s;
                         """, (client_data,))
            client_id = cur.fetchall()[0][0]
            result_search_client(cur, 'client_id', client_id)
        else:
            print('ОТМЕНА: выбранный ключ не соответствует ни одной записи')


def result_search_client(cur, attribute_name, client_data):
    cur.execute(f"""
                SELECT client_id, first_name, last_name, email
                  FROM clients
                 WHERE {attribute_name} = %s;
                """, (client_data,))
    clients_list = cur.fetchall()
    print('**************************')
    print(f'Результат поиска:')
    for client in clients_list:
        print('**************************')
        print(f'Клиент: {client[1]} {client[2]}\n'
              f'email: {client[3]}')
        cur.execute("""
                    SELECT phone
                      FROM phones
                     WHERE client_id = %s
                    """, (client[0],))
        for phones in cur.fetchall():
            print(f'Номер телефона: {phones[0]}')


def client_phones(conn_, client_id):
    phones_dict = dict()
    count = 1
    with conn_.cursor() as cur:
        cur.execute("""
                    SELECT phone
                      FROM phones
                     WHERE client_id = %s
                    """, (client_id, ))
        for phone in cur.fetchall():
            phones_dict[count] = phone[0]
            count += 1
    return phones_dict


def phone_info(conn_, client_id):
    phones_dict = client_phones(conn_, client_id)
    print('****************************')
    print('Информация о номере телефона')
    for key, phone in phones_dict.items():
        print(f'ключ {key} соответствует номеру телефона {phone}')

    key_ = input('введите ключ, соответствующий номеру телефона: ')
    return key_


def search_id(conn_, email):
    with conn_.cursor() as cur:
        cur.execute("""
                    SELECT client_id
                      FROM clients
                     WHERE email = %s;
                    """, (email, ))

        return cur.fetchone()[0]


def is_number(str_):
    try:
        float(str_)
        return True
    except ValueError:
        return False


def email_check(conn, email):
    is_boolean = False
    with conn.cursor() as cur:
        cur.execute(f"""
                    SELECT email
                      FROM clients;
                    """)

        for email_ in cur.fetchall():
            if email_[0] in email:
                is_boolean = True
    return is_boolean


def management_bd(numb_, name):

    while True:
        if numb_ == '1':
            create_delete_db(name, 'DROP', 'IF EXISTS')
            print(f'База {name} удалена')
            break
        elif numb_ == '2':
            create_delete_db(name, 'DROP', 'IF EXISTS')
            create_delete_db(name, 'CREATE', '')
            print(f'База {name} создана')
            break
        elif (numb_ == '3' or numb_ == '4' or numb_ == '5'
              or numb_ == '6' or numb_ == '7' or numb_ == '8'
              or numb_ == '9'):
            with psycopg2.connect(database=name, user='postgres',
                                  password='6056') as conn_:
                if numb_ == '3':
                    create_tables(conn_)
                    break
                elif numb_ == '4':
                    add_client(conn_)
                    break
                elif numb_ == '5':
                    email = input('Введите email клиента: ')
                    if email_check(conn_, email):
                        add_phone(conn_, email)
                    else:
                        print(f'ОТМЕНА: "{email}" нет в записях')
                    break
                elif numb_ == '6':
                    email = input('Введите email клиента: ')
                    if email_check(conn_, email):
                        menu_update_db(conn_, email)
                    else:
                        print(f'ОТМЕНА: "{email}" нет в записях')
                    break
                elif numb_ == '7':
                    email = input('Введите email клиента: ')
                    if email_check(conn_, email):
                        delete_phone(conn_, email)
                    else:
                        print(f'ОТМЕНА: "{email}" нет в записях')
                    break
                elif numb_ == '8':
                    email = input('Введите email клиента: ')
                    if email_check(conn_, email):
                        delete_client(conn_, email)
                    else:
                        print(f'ОТМЕНА: "{email}" нет в записях')
                    break
                elif numb_ == '9':
                    search_client(conn_)
                    break
        else:
            print('ОТМЕНА: функция не выбрана')
            break


if __name__ == '__main__':
    db_name = input('Введите название Базы Данных: ')
    num_ = input('* 1 - Удалить базу данных \n'
                 '* 2 - Создать базу данных\n'
                 '* 3 - Создать структуру БД\n'
                 '* 4 - Добавить клиента\n'
                 '* 5 - Добавить телефон для существующего клиента\n'
                 '* 6 - Изменить данные о клиенте\n'
                 '* 7 - Удалить телефон для существующего клиента\n'
                 '* 8 - Удалить существующего клиента\n'
                 '* 9 - Найти клиента\n'
                 'Выберите номер функции: '
                 )
    management_bd(num_, db_name)
