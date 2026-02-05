import sqlite3
import os

# Delete old database if it exists to start fresh
if os.path.exists("products.db"):
    os.remove("products.db")

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        category TEXT,
        image TEXT,
        description TEXT
    )
''')

# THESE PRICES NOW MATCH YOUR HTML EXACTLY
products = [
    # GROCERIES
    (1, 'Basmati Rice 10kg', 2000, 'groceries', '/static/product/basmati.webp', 'Naturally aromatic long-grain basmati rice with a soft, fluffy texture.'),
    (2, 'Wheat Flour 50kg', 6000, 'groceries', '/static/product/wheat floor.webp', 'Finely milled whole wheat flour for soft roti and chapati.'),
    (3, 'Cooking Oil 1L', 2500, 'groceries', '/static/product/oil.webp', 'Pure and refined cooking oil for healthy meals.'),
    (4, 'Beans 5kg', 1200, 'groceries', '/static/product/beans.webp', 'Fresh beans rich in protein and fiber.'),
    (5, 'Masala 5kg', 1500, 'groceries', '/static/product/masala.webp', 'A balanced blend of aromatic spices.'),
    (6, 'Biryani Masala 5kg', 2300, 'groceries', '/static/product/biryani masala.webp', 'Authentic spice mix for restaurant-style Biryani.'),
    (7, 'Sugar 5kg', 600, 'groceries', '/static/product/suger.webp', 'Refined white sugar for tea and desserts.'),
    (8, 'Olper Milk 500ml', 400, 'groceries', '/static/product/olper.webp', 'Fresh and creamy milk pack.'),
    (9, 'Almond 5kg', 3000, 'groceries', '/static/product/almond.webp', 'Premium quality crunchy almonds.'),
    (10, 'Pista 5kg', 4000, 'groceries', '/static/product/pista.webp', 'High-quality pistachios with rich taste.'),
    
    # FOOD
    (11, 'Burger', 700, 'food', '/static/product/burger.webp', 'Juicy and flavorful chicken burger.'),
    (12, 'Noodles', 200, 'food', '/static/product/noodle.webp', 'Quick-cooking spicy noodles.'),
    (13, 'Biscuits', 100, 'food', '/static/product/biscuit.webp', 'Crispy biscuits perfectly baked.'),
    (14, 'Chocolate', 500, 'food', '/static/product/chocolates.webp', 'Rich and smooth milk chocolate.'),
    (15, 'Tea', 200, 'food', '/static/product/tea.webp', 'Strong aroma premium tea leaves.'),
    (16, 'Coffee', 350, 'food', '/static/product/cofee.webp', 'Finely roasted instant coffee.'),
    (17, 'Breads', 250, 'food', '/static/product/breads.webp', 'Soft and fresh bread for breakfast.'),
    (18, 'Eggs', 800, 'food', '/static/product/eggs.webp', 'Farm fresh organic eggs.'),
    (19, 'Butter', 450, 'food', '/static/product/butter.webp', 'Creamy salted butter.'),
    (20, 'Yogurt', 200, 'food', '/static/product/yougrt.webp', 'Fresh and thick yogurt.'),

    # ELECTRONICS
    (21, 'TV', 15000, 'electronics', '/static/product/tv.webp', 'HD LED Television with clear picture.'),
    (22, 'Smartphone', 45000, 'electronics', '/static/product/phone.webp', 'Fast processor and high quality camera.'),
    (23, 'Headphones', 8000, 'electronics', '/static/product/headphone.webp', 'Noise cancelling bass headphones.'),
    (24, 'Laptop', 100000, 'electronics', '/static/product/laptop.webp', 'High performance laptop for work and gaming.'),
    (25, 'Tablet', 20000, 'electronics', '/static/product/tab.webp', 'Big screen tablet for entertainment.'),
    (26, 'Smart Watch', 3500, 'electronics', '/static/product/smrtwatch.webp', 'Fitness tracking smart watch.'),
    (27, 'Power Bank', 4000, 'electronics', '/static/product/poerbnk.webp', 'Fast charging portable battery.'),
    (28, 'CCTV Camera', 10000, 'electronics', '/static/product/cctv.webp', 'Security camera with night vision.'),
    (29, 'Microwave Oven', 7000, 'electronics', '/static/product/oven.webp', 'Quick heating microwave oven.'),
    (30, 'Iron', 3500, 'electronics', '/static/product/iron.webp', 'Heavy duty steam iron.'),

    # TOOLS
    (31, 'Hammer', 800, 'tools', '/static/product/hmer.webp', 'Strong steel hammer with grip.'),
    (32, 'Screwdriver', 250, 'tools', '/static/product/screwdriver.webp', 'Multi-head screwdriver.'),
    (33, 'Electric Drill', 20000, 'tools', '/static/product/drill.webp', 'Powerful cordless drill.'),
    (34, 'Safety Gloves', 700, 'tools', '/static/product/safty.webp', 'Protective gloves for heavy work.'),
    (35, 'Measuring Tape', 800, 'tools', '/static/product/tape.webp', 'Accurate 5m measuring tape.'),
    (36, 'Wrench', 899, 'tools', '/static/product/wrench.webp', 'Adjustable heavy duty wrench.'),
    (37, 'Cutter', 499, 'tools', '/static/product/cutter.webp', 'Sharp utility cutter.'),
    (38, 'Welding Machine', 15999, 'tools', '/static/product/welding.webp', 'Portable welding machine.'),
    (39, 'Hand Saw', 700, 'tools', '/static/product/handsaw.webp', 'Sharp wood cutting saw.'),
    (40, 'Drill Bits', 700, 'tools', '/static/product/drillbits.webp', 'Set of durable drill bits.')
]

cursor.executemany('INSERT INTO products (id, name, price, category, image, description) VALUES (?, ?, ?, ?, ?, ?)', products)
conn.commit()
conn.close()

print("Database updated successfully with NEW PRICES!")