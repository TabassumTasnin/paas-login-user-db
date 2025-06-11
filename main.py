from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to PostgreSQL using Render's environment variables
conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
)

cur = conn.cursor()

# Home route
@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", user=session["username"])
    return redirect("/login")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect("/login")
    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        if user:
            session["username"] = username
            return redirect("/")
        return "Login failed"
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
