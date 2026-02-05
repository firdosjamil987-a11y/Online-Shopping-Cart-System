import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ---------------- PRODUCTS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    category TEXT,
    image TEXT,
    description TEXT
)
""")

# ---------------- CART TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    product_name TEXT,
    price INTEGER,
    quantity INTEGER
)
""")

# ---------------- ORDERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    product_name TEXT,
    price INTEGER,
    quantity INTEGER
)
""")

# ---------------- CLOSE CONNECTION ----------------
conn.commit()
conn.close()

print("✅ All tables created successfully")
