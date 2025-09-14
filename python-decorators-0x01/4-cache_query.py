import time
import sqlite3 
import functools


query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        
        cache_key = query
        
        if cache_key in query_cache:
            print("Fetching from cache...")
            return query_cache[cache_key]
        
        print("Fetching from database...")
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper
    
    

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")

users_again = fetch_users_with_cache(query="SELECT * FROM users")