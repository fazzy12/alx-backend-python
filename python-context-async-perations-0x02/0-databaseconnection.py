import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()
            
        

if __name__ == '__main__':
    with DatabaseConnection() as cursor:
       cursor.execute("SELECT * FROM users")
       results = cursor.fetchall()
       print(results)
