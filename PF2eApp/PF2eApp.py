#using base boilerplate code from finance assignment
import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from helpers import apology, login_required
from flask_session import Session


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(16)
app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'
# Check Configuration section for more details
app.config.from_object(__name__)
Session(app)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello, World!"

@app.route('/login')
def login():
    # connect database
    con = sqlite3.connect('pathfinder.db')
    # create cursor object
    cur = con.cursor()
    
    # Log user in

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], (request.form.get("password"),)):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        con.commit()
        con.close()

        # Redirect user to home page
        return redirect("/")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # connect database
    con = sqlite3.connect('pathfinder.db', check_same_thread=False)
    # create cursor object
    cur = con.cursor()

    if request.method == "POST":
        """Register user"""
        # Query database for username to ensure unique
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cur.fetchall()
        cur.close()
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Ensure passwords match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        # Ensure passwords used
        if request.form.get("confirmation") == "" or request.form.get("password") == "" or request.form.get("username") == "":
            return apology("field cannot be blank", 400)

        # insert user data into user table in database
        usernameinsert = request.form.get("username")
        hashinsert = generate_password_hash(request.form.get("password"))
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (usernameinsert, hashinsert))
        cur.close()

        # get info about user from table
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        newrows = cur.fetchall()
        cur.close()

        # Remember which user has logged in
        session["user_id"] = newrows[0]["id"]
        tablename = newrows[0]["username"]+"characters"
        # create table for users characters
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE ? (name VARCHAR(255), class VARCHAR(255), str VARCHAR(255), dex VARCHAR(255), con VARCHAR(255), int VARCHAR(255), wis VARCHAR(255), cha VARCHAR(255), level VARCHAR(255))", (tablename,))

        con.commit()
        con.close()
        # Redirect user to home page
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html")


def errorhandler(e):
    # Handle error
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()