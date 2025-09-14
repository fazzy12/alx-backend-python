import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
                
        if self.params:
            cursor.execute(self.query, self.params)
        else:
            cursor.execute(self.query)
                    
        self.results = cursor.fetchall()
        return self.results
    

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


if __name__ == '__main__':
    try:
        query_string = "SELECT * FROM users WHERE age > ?"
        with ExecuteQuery('users.db', query_string, (25,)) as users:
            print("Users older than 25:")
            print(users)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}. Did you create the users table?")