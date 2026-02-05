from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key_for_login"

DB_NAME = "products.db"

# ---------------- DATABASE HELPER ----------------

def get_db():
    return sqlite3.connect(DB_NAME)

def get_products():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products


# ---------------- AUTH ROUTES ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid login details"

    return render_template("login.html")

@app.route("/reset_password", methods=["POST"])
def reset_password():
    username = request.form["username"]
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]

    conn = get_db()
    cursor = conn.cursor()

    # Check old password
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, old_password)
    )
    user = cursor.fetchone()

    if user:
        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_password, username)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    else:
        conn.close()
        return "Old password is incorrect"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            conn.close()
            return "Username already exists"

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



# ---------------- MAIN PAGES ----------------

@app.route('/')
def home():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)


# ---------------- PRODUCT DETAILS ----------------

@app.route('/product/<int:id>')
def product_details(id):
    conn = sqlite3.connect('products.db')
    
    # --- THIS IS THE MAGIC LINE ---
    # It allows you to use {{ product.name }} instead of {{ product[1] }}
    conn.row_factory = sqlite3.Row 
    # ------------------------------
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return render_template('product_details.html', product=product)
    else:
        return "Product not found", 404

# ---------------- BUY NOW (FIXED) ----------------

@app.route('/buy_now', methods=['POST'])
def buy_now():
    if "user" not in session:
        return redirect(url_for("login"))

    product_id = request.form['product_id']

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price FROM products WHERE id=?",
        (product_id,)
    )
    product = cursor.fetchone()
    conn.close()

    session["cart"] = {
        str(product["id"]): {
            "name": product["name"],
            "price": product["price"],
            "qty": 1
        }
    }

    return redirect(url_for("checkout"))


# ---------------- CART ----------------

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    # 1. Connect to DB to get the correct Name, Price, and Image
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    # 2. Add to session (Cart)
    if product:
        # Get the current cart or create a new one
        cart = session.get('cart', {})
        
        id_str = str(product_id)

        if id_str in cart:
            cart[id_str]['qty'] += quantity
        else:
            cart[id_str] = {
                'name': product['name'],
                'price': product['price'],
                'image': product['image'], # This saves the image path to the cart
                'qty': quantity
            }

        session['cart'] = cart
        session.modified = True
        
    return redirect(url_for('cart'))


@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total)


@app.route("/increase/<item>")
def increase(item):
    session["cart"][item]["qty"] += 1
    session.modified = True
    return redirect(url_for("cart"))


@app.route("/decrease/<item>")
def decrease(item):
    session["cart"][item]["qty"] -= 1
    if session["cart"][item]["qty"] <= 0:
        session["cart"].pop(item)
    session.modified = True
    return redirect(url_for("cart"))


# ---------------- CHECKOUT ----------------

@app.route('/checkout')
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())

    delivery_fee = 200
    grand_total = total + delivery_fee

    return render_template(
        'checkout.html',
        cart=cart,
        total=total,
        delivery_fee=delivery_fee,
        grand_total=grand_total
    )


# ---------------- PAYMENT ----------------

@app.route("/payment")
def payment():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("payment.html")


@app.route("/payment_success", methods=["POST"])
def payment_success():
    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("home"))

    conn = get_db()
    cursor = conn.cursor()

    for item in cart.values():
        cursor.execute("""
            INSERT INTO orders (username, product_name, price, quantity)
            VALUES (?, ?, ?, ?)
        """, (session["user"], item["name"], item["price"], item["qty"]))

    conn.commit()
    conn.close()

    session.pop("cart")

    return render_template("payment_success.html")


# ---------------- ORDERS ----------------

@app.route("/orders")
def orders():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE username=?",
        (session["user"],)
    )
    orders = cursor.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
