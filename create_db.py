import sqlite3

# connect database
con = sqlite3.connect('pathfinder.db')
# create cursor object
cur = con.cursor()

# cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, username VARCHAR(255) NOT NULL UNIQUE, hash VARCHAR(25) NOT NULL)')
cur.execute("CREATE TABLE characters (characterid INTEGER PRIMARY KEY NOT NULL, playerid INTEGER REFERENCES users, Name VARCHAR(255), Class VARCHAR(255), Str INT, Dex INT, Con INT, Int INT, Wis INT, Cha INT, Level INT, Backstory VARCHAR(255))")
# Save (commit) the changes
con.commit()
con.close()