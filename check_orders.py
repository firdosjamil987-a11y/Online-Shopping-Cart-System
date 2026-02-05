import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()

print("ORDERS TABLE DATA:")
for row in rows:
    print(row)

conn.close()
