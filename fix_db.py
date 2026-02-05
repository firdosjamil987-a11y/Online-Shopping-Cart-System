import sqlite3

def setup():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create a test user so you can log in
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))
        print("✅ Success: 'users' table created and test user 'admin' added.")
    except sqlite3.IntegrityError:
        print("✅ Table already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup()