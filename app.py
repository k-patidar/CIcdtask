from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database setup
def init_db():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, name TEXT, price REAL, image TEXT)")
    conn.commit()
    conn.close()

# Home
@app.route("/")
def index():
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("ecommerce.db")
        c = conn.cursor()
        c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",(username,password,"customer"))
        conn.commit()
        conn.close()
        flash("Registered successfully! Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("ecommerce.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            if user[3] == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("index"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Admin Dashboard
@app.route("/admin")
def admin():
    if "role" in session and session["role"] == "admin":
        return render_template("admin.html")
    return redirect(url_for("login"))

# Add Product
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "role" in session and session["role"] == "admin":
        if request.method == "POST":
            name = request.form["name"]
            price = request.form["price"]
            image = request.files["image"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            conn = sqlite3.connect("ecommerce.db")
            c = conn.cursor()
            c.execute("INSERT INTO products(name,price,image) VALUES(?,?,?)",(name,price,filename))
            conn.commit()
            conn.close()
            flash("Product added successfully!")
            return redirect(url_for("admin"))
        return render_template("add_product.html")
    return redirect(url_for("login"))

# Cart (very simple - just demo)
@app.route("/cart/<int:product_id>")
def cart(product_id):
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    return render_template("cart.html", product=product)

if __name__ == "__main__":
    init_db()
    # Add default admin
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users(username,password,role) VALUES('admin','admin','admin')")
    conn.commit()
    conn.close()
    app.run(debug=True)
