import sqlite3

# connect database
con = sqlite3.connect('pathfinder.db')
# create cursor object
cur = con.cursor()

cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, username VARCHAR(255) NOT NULL UNIQUE, hash VARCHAR(25) NOT NULL)')
cur.execute("CREATE TABLE characters (characterid INTEGER PRIMARY KEY NOT NULL, playerid INTEGER REFERENCES users, name VARCHAR(255), class VARCHAR(255), str VARCHAR(255), dex VARCHAR(255), con VARCHAR(255), int VARCHAR(255), wis VARCHAR(255), cha VARCHAR(255), level VARCHAR(255), backstory VARCHAR(255))")
# Save (commit) the changes
con.commit()
con.close()