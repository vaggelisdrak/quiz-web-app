from flask import Flask, render_template, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import random

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def contact():
    return render_template("about.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    option = request.form.get('radio')
    score = 5 #the game hasn't started yet,when it finishes the result updates to a number >=0
    now = datetime.now()
    dt= now.strftime("%d/%m/%Y %H:%M:%S")# dd/mm/YY H:M:S
    time = '00:00'

    conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute("INSERT INTO PLAYERS(name, email, level, score, date, time) VALUES (?, ?, ?, ?, ?, ?)",(first_name, email, option, score, dt, time))
    c.execute('SELECT name,email,level,score,date,time FROM PLAYERS')
    players = c.fetchall()

    player = []
    games_played=0
    for n,e,l,s,d,t in players[:-1]:
        if n==first_name and e==email:
            print(n,e,l,s,d,t)#all the games this player has played
            games_played+=1
            player.append((n,e,l,s,d,t))

    player.reverse()
    conn.commit()
    conn.close()
    if not player:
        #new players start the quiz right away without looking at their stats
        return redirect("/questions")
    else:
        return render_template("form.html",player=player,games=games_played)

def send_email(email):
    try:
        message = "Thank you for participating!"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("botpython210@gmail.com", "fhfghf56gh4f6gh5f5ghsf6gh46fgh5")
        server.sendmail("botpython210@gmail.com", email ,message)
        print('Email sent!')
    except:
        print('Something went wrong...')

@app.route('/questions')
def questions():
    conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT name,email,level,score,date,time FROM PLAYERS')
    players = c.fetchall()
    level=''
    for n,e,l,s,d,t in players:#the difficulty level that the player chose is the last value of the level's database
        level=l

    conn.close()

    conn = sqlite3.connect('QUESTIONS.db', check_same_thread=False)
    c = conn.cursor()
    random_questions =[]
    options =[]
    c.execute('SELECT id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse FROM QUESTIONS')
    questions = c.fetchall()

    if level=='easy':
        mylist = [i for i in range(1,21)]

    if level=='medium':
        mylist = [i for i in range(21,41)]

    x = random.sample(mylist,5)
    print(x)
    for i,l,q,a1,a2,a3,a4,c,ex,re in questions:
        if i in x:
            random_questions.append((i,l,q,a1,a2,a3,a4,c,ex,re))
            options.append((a1,a2,a3,a4))
    conn.close()
    return render_template("questions.html",questions=random_questions,options=options)

if __name__ == "__main__":
    app.run(debug=True)