import sqlite3

def setup_database():
    """Create a database and a users table for testing."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

    # Insert some dummy data to work with
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
        cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
        conn.commit()
    except sqlite3.IntegrityError:
        print("Data already exists.")
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup complete.")