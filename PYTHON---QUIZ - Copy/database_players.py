import sqlite3

def create_table():
    conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS PLAYERS(name TEXT, email TEXT, level TEXT, score INT, date TEXT, time TEXT,points INT, id INTEGER PRIMARY KEY AUTOINCREMENT)')
    c.close()
    conn.close()

create_table()