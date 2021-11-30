import sqlite3

# connect database
con = sqlite3.connect('pathfinder.db')
# create cursor object
cur = con.cursor()

cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, username VARCHAR(255) NOT NULL UNIQUE, hash VARCHAR(25) NOT NULL)')

# Save (commit) the changes
con.commit()