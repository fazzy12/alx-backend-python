#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='virgin123'
        )
        
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        connection: MySQL connection object connected to ALX_prodev database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='virgin123',
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file_path):
    """
    Inserts data from CSV file into the database.
        
    Args:
        connection: MySQL connection object
        csv_file_path: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
            
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age) 
        VALUES (%s, %s, %s, %s)
        """
            
        data_to_insert = []
            
        # Read CSV file and prepare data
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
                
            for row in csv_reader:
                # Handle UUID generation if not present
                user_id = row.get('user_id', str(uuid.uuid4()))
                    
                data_tuple = (
                    user_id,
                    row['name'],
                    row['email'],
                    int(float(row['age']))
                )
                data_to_insert.append(data_tuple)
            
        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
            print(f"{len(data_to_insert)} records inserted successfully.")
        else:
            print("No data to insert.")
            
        cursor.close()
            
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found")
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")