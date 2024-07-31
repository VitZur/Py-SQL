import psycopg2
from psycopg2 import OperationalError

def create_db():
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name  VARCHAR(50),
                email VARCHAR(100)           
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                phone VARCHAR(20)        
            )
        ''')
        
        conn.commit()
    except OperationalError as e:
         print(f'An error occurred: {e}')
    finally:
        if cursor:
              cursor.close()
        if conn:
              conn.close()
              

def add_client(first_name, last_name, email):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        cursor.execute('''
             INSERT INTO clients (first_name, last_name, email) 
             VALUES (%s, %s, %s)
        ''', (first_name, last_name, email))

        conn.commit()
    except OperationalError as e:
        print(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_phone(client_id, phone):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        cursor.execute('''
             INSERT INTO phones (client_id, phone) VALUES (%s, %s)
           ''', (client_id, phone))

        conn.commit()
    except OperationalError as e:
        print(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_client(client_id, first_name=None, last_name=None, email=None):     
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        if first_name:
            cursor.execute('''
                UPDATE clients
                SET first_name = %s
                WHERE id = %s
            ''', (first_name, client_id))

        if last_name:
            cursor.execute('''
                UPDATE clients
                SET last_name = %s
                WHERE id = %s
            ''', (last_name, client_id))

        if email:
            cursor.execute('''
                UPDATE clients
                SET email = %s
                WHERE id = %s
            ''', (email, client_id))

        conn.commit()
        
    except OperationalError as e:
        print(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_client(client_id):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM phones WHERE client_id = %s
        ''', (client_id,))
        cursor.execute('''
            DELETE FROM clients WHERE id = %s
        ''', (client_id,))
        conn.commit()
    except OperationalError as e:
        print(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_phone(client_id, phone):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM phones
            WHERE client_id = %s AND phone = %s
        ''', (client_id, phone))
        
        conn.commit()
        
    except OperationalError as e:
        print(f'An error occurred: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def find_client(client_id=None, first_name=None, last_name=None, email=None, phone=None):
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='24bfea9d',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        query = "SELECT c.* FROM clients c"
        conditions = []
        params = []

        if phone:
            query += " JOIN phones p ON c.id = p.client_id"
            conditions.append('p.phone = %s')
            params.append(phone)

        if client_id is not None:
            conditions.append('c.id = %s')
            params.append(client_id)
        if first_name:
            conditions.append('c.first_name = %s')
            params.append(first_name)
        if last_name:
            conditions.append('c.last_name = %s')
            params.append(last_name)
        if email:
            conditions.append('c.email = %s')
            params.append(email)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        cursor.execute(query, params)
        results = cursor.fetchall()

    except OperationalError as e:
        print(f'An error occurred: {e}')
        results = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return results

if __name__ == "__main__":
    create_db()

    add_client('John', 'Doe', 'john.doe@example.com')
    add_client('Jane', 'Smith', 'jane.smith@example.com')

    add_phone(1, '1234567890')
    add_phone(2, '1234567890')
    add_phone(3, '5555555555')

    update_client(1, first_name='Johnny')

    find_1 = find_client(first_name='Johnny')
    find_2 = find_client(phone='5555555555')

    for result in find_1:
        print(result)
    for result in find_2:
        print(result)

    delete_client(2)
