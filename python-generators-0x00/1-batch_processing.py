#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="virgin123",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data"
        cursor.execute(query)
        
        
        while True:
            batch = cursor.fetchmany(size=batch_size)
            if not batch:
                break
            yield batch
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if  cursor:
                cursor.close()
        if  connection and connection.is_connected():
                connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
    
