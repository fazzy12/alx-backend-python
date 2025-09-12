#!/usr/bin/python3
import mysql.connector
from uuid import uuid4

seed = __import__('seed')

def paginate_users(page_size, offset):
    
    connection = None
    cursor = None
    
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        querry = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(querry)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return[]
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def lazy_pagination(page_size):
    offset = 0
    
    while True:
        page_of_users = paginate_users(page_size, offset)
        if not page_of_users:
            break
        yield page_of_users
        offset += page_size