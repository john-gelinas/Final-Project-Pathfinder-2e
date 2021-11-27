#using base boilerplate code from finance assignment

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

# ~not working becuase flask_session will not import~
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# connect database
con = sqlite3.connect('pathfinder.db')
# create cursor object
cur = con.cursor()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello, World!"

@app.route('/login')
def login():
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
        rows = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    if request.method == "POST":
        """Register user"""
        # Query database for username to ensure unique
        rows = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
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
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", usernameinsert, hashinsert)

        # get info about user from table
        newrows = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = newrows[0]["id"]
        histtable = newrows[0]["username"]+"history"
        # create table for users stocks
        cur.execute(
            "CREATE TABLE ? (StockID INTEGER NOT NULL PRIMARY KEY, StockSymbol VARCHAR(255) NOT NULL UNIQUE, StockAmount INTEGER NOT NULL)", newrows[0]["username"])
        # create table for user history
        cur.execute(
            "CREATE TABLE ? (TransactionID INTEGER NOT NULL PRIMARY KEY, StockSymbol VARCHAR(255) NOT NULL, StockAmount INTEGER NOT NULL, TransactionTime VARCHAR(255) NOT NULL, TransactionType VARCHAR(255) NOT NULL, StockPrice DOUBLE(8, 2) NOT NULL)", histtable)

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
