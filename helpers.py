from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", error = code, message = message)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def scrub(table_name):
    return ''.join( chr for chr in table_name if chr.isalnum() or chr == " " or chr == "." )
# From Donald Miner for scrubbing special characters from https://stackoverflow.com/questions/3247183/variable-table-name-in-sqlite

def sqlselect(query):
    # connect database
    con = sqlite3.connect('pathfinder.db')
    # create cursor object
    cur = con.cursor()
    cur.execute(query)
    rowcount = cur.rowcount
    if rowcount == 0:
        data = []
    else:
        data = cur.fetchall()
    cur.close()
    con.close()
    return data

# convert cursor object output to dictionary
def dictfactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d