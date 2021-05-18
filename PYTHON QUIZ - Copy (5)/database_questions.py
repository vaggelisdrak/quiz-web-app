import sqlite3

def create_table():
    conn = sqlite3.connect('QUESTIONS.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS QUESTIONS(id INT, level TEXT, question TEXT, ans1 TEXT, ans2 TEXT, ans3 TEXT, ans4 TEXT, correctans TEXT, explanation TEXT, reccourse TEXT)')
    id = 0 
    question='---'
    level = 'easy'
    ans1='---'
    ans2='---'
    ans3='---'
    ans4='---'
    correctans='---'
    explanation='---'
    reccourse='---'
    for i in range(1,61):
        id=i
        c.execute("INSERT INTO QUESTIONS(id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse))
        conn.commit()
    c.close()
    conn.close()

create_table()