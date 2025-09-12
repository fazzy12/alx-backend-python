#!/usr/bin/python3

import mysql.connector

seed = __import__('seed')

def stream_user_ages():
    connection = None
    cursor = None
    
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        cursor.execute("SELECT age FROM user_data")
        
        for row in cursor:
            yield row['age']
            
            
    except mysl.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            

def calculate_average_age():
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    if count == 0:
        return 0
    return total_age / count


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
