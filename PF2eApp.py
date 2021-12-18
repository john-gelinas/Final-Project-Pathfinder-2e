#using base boilerplate code from finance assignment
import os
import sys
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from helpers import apology, login_required, sqlselect, scrub, dictfactory
from flask_session import Session
from math import floor


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
    user = session["user_id"]
    return render_template('index.html', user=user)

@app.route('/home')
def home():
    return redirect('/')

@app.route('/characters')
@login_required
def characters():
    if request.method == "GET":
        user = session["user_id"]
        user = scrub(user)
        query = "SELECT id FROM users WHERE username = '{}'".format(user)
        playerid = sqlselect(query)[0][0]
        # get and display characters from db
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("SELECT Name FROM characters WHERE playerid = {}".format(playerid))
        chardata = cur.fetchall()
        cur.close()
        con.close()
        app.logger.info(chardata)    
        return render_template('characters.html', chardata=chardata)

    
@app.route('/character/<name>', methods=["GET", "POST"])
def character(name):
    # get character data from database
    user = session["user_id"]
    name = scrub(name)
    user = scrub(user)
    query = "SELECT id FROM users WHERE username = '{}'".format(user)
    playerid = sqlselect(query)[0][0]
    con = sqlite3.connect('pathfinder.db')
    con.row_factory = dictfactory
    cur = con.cursor()
    cur.execute("SELECT * FROM characters WHERE name = '{}' AND playerid = {}".format(name, playerid))
    chardata = cur.fetchall()[0]
    cur.close()
    con.close()
    
    if request.method == "GET":
        chardata["Str Mod"] = floor((chardata["Str"] - 10)/2)
        chardata["Dex Mod"] = floor((chardata["Dex"] - 10)/2)
        chardata["Con Mod"] = floor((chardata["Con"] - 10)/2)
        chardata["Int Mod"] = floor((chardata["Int"] - 10)/2)
        chardata["Wis Mod"] = floor((chardata["Wis"] - 10)/2)
        chardata["Cha Mod"] = floor((chardata["Cha"] - 10)/2)

        proficiencies = {}
        proficiencies["Untrained"] = 0
        proficiencies["Trained"] = chardata["Level"] + 2
        proficiencies["Expert"] = chardata["Level"] + 4
        proficiencies["Master"] = chardata["Level"] + 6
        proficiencies["Legendary"] = chardata["Level"] + 8

        return render_template("viewcharacter.html", chardata = chardata, proficiencies = proficiencies)

    if request.method == "POST":
        field = request.form.get("field")
        field = scrub(field)
        value = request.form.get(field)
        value = scrub(value)
        app.logger.info(field)    
        app.logger.info(value)    
        con = sqlite3.connect('pathfinder.db') 
        cur = con.cursor()
        query = "UPDATE characters SET '{}' = '{}' WHERE Name = '{}' AND playerid = '{}'".format(field, value, name, playerid)
        cur.execute(query)
        con.commit()
        cur.close()
        con.close()
        charpage = "/character/" + name
        return redirect(charpage)


@app.route('/newcharacter', methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        #display form
        return render_template("newcharacter.html")

    if request.method == "POST":
        user = session["user_id"]
        user = scrub(user)
        query = "SELECT id FROM users WHERE username = '{}'".format(user)
        playerid = sqlselect(query)[0][0]    
        #pass form to db, display character
        chardata = dict()
        chardata["name"] = request.form.get("Name")
        chardata["class"] = request.form.get("Class")
        chardata["str"] = request.form.get("Str")
        chardata["dex"] = request.form.get("Dex")
        chardata["con"] = request.form.get("Con")
        chardata["int"] = request.form.get("Int")
        chardata["wis"] = request.form.get("Wis")
        chardata["cha"] = request.form.get("Cha")
        chardata["level"] = request.form.get("Level")
        chardata["backstory"] = request.form.get("Backstory")
        #add data to database
        #connect db
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("INSERT INTO characters (playerid, Name, Class, Str, Dex, Con, Int, Wis, Cha, Level, Backstory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerid, chardata["name"], chardata["class"], chardata["str"], chardata["dex"], chardata["con"], chardata["int"], chardata["wis"], chardata["cha"], chardata["level"], chardata["backstory"]))
        con.commit()
        cur.close
        con.close

        charpage = "/character/" + chardata["name"]
        return redirect(charpage)


@app.route('/login', methods=["GET", "POST"])
def login():
    app.logger.info('testing info log')    
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
        app.logger.info('here2')
        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cur.fetchall()
        cur.close()
        con.close()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], (request.form.get("password"))):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][1]
        flash("Logged In")
        # Redirect user to home page
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

@app.route("/dice")
def dice():
    return render_template("dice.html")


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
        user = request.form.get("username")
        userscrubbed = scrub(user)
        if user != userscrubbed:
            return apology("username may not contain special characters or spaces")
        query = "SELECT * FROM users WHERE username = '{}'".format(user)
        rows = sqlselect(query)
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
        con.commit()
        con.close()

        # get info about user from table
        con = sqlite3.connect('pathfinder.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        newrows = cur.fetchall()
        cur.close()

        # Remember which user has logged in
        session["user_id"] = newrows[0][1]

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