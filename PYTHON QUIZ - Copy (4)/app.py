from flask import Flask, render_template, request, redirect, session, url_for
import smtplib
from datetime import datetime, timedelta
import sqlite3
import random
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-string'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    if session['first_name'] and session['email']:#remember the previous login
        first_name = session['first_name']
        email = session['email']
        return render_template("login.html",first_name=first_name,email=email)
    else:
        return render_template("login.html")

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    option = request.form.get('radio')
    print(option)
    session['first_name'] = first_name
    session['email'] = email
    session['lvl'] = option
    score = 0 #the game hasn't started yet,when it finishes the result updates to a number >=0
    now = datetime.now()
    dt= now.strftime("%d/%m/%Y %H:%M:%S")# dd/mm/YY H:M:S
    time = '00:00'

    conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute("INSERT INTO PLAYERS(name, email, level, score, date, time) VALUES (?, ?, ?, ?, ?, ?)",(first_name, email, option, score, dt, time))
    print('last_row_id: ',c.lastrowid)
    session['id'] = c.lastrowid
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
    if not player:#if it is a new player
        return redirect(url_for("start"))
    else:
        print(player[0])
        return render_template("form.html",player=player,games=games_played,level=option,last_level=player[0][2])

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

@app.route('/start')
def start():
    level = session.get("lvl")
    conn = sqlite3.connect('QUESTIONS.db', check_same_thread=False)
    c = conn.cursor()
    random_questions = []
    options = []
    ids =[]
    mylist = []
    c.execute('SELECT id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse FROM QUESTIONS')
    questions = c.fetchall()

    if level=='easy':
        #mylist = [i for i in range(1,21)]
        for i in range(1,21):
            mylist.append(i)

    if level=='medium':
        #mylist = [i for i in range(21,41)]
        for i in range(21,41):
            mylist.append(i)

    if level=='hard':
        #mylist = [i for i in range(41,61)]
        for i in range(41,61):
            mylist.append(i)
        
    print(mylist)
    x = random.sample(mylist,5)
    print(x)
    for i,l,q,a1,a2,a3,a4,c,ex,re in questions:
        if i in x:
            random_questions.append((i,l,q,a1,a2,a3,a4,c,ex,re))
            options.append((a1,a2,a3,a4))
            ids.append(i)
    conn.close()

    print(ids)
    print(random_questions)
    session["questions"] = random_questions
    session["displayed_question"] = random_questions
    session["score"] = 0
    session["count"] = 0
    session["difficulty"] = level
    #session["last_id"] = ids[0]
    return redirect(url_for('questions', id=ids.pop()))

@app.route('/questions/<id>')
def questions(id):
    print("ROUTE /quiz", id)

    # ανάκτησε από το session την κατάσταση...
    score = session.get("score", 0)
    count = session.get("count",0)
    level = session.get("difficulty")
    questions = session.get("questions", []) #random questions
    #last_id = session.get("last_id")
    #displayed_question = session.get("displayed_question", [])

    if request.query_string: # ο χρήστης απάντησε
        reply = request.args.get("answer")
        '''f = open("store_data.txt", "w")
        f.write(reply)
        f.close()'''
        correct = session["displayed_question"][7]
        print(reply,correct)
        new_score = 0
        if reply == correct:
            new_score=1
        score += new_score
        print('score is...', score)
        #print(questions)
        if questions: 
            next_question = questions[-1]
        else:
            next_question = "end"
        session["score"] = score
        ## να δώσουμε ανάδραση για την απάντηση και σκορ
        return render_template('question.html', question = session["displayed_question"],
            id = id, next_question = next_question, button="Next",
            disabled = "disabled",correct=correct,reply=reply)

    else: # πρέπει να στείλουμε στον χρήστη την ερώτηση
        try:
            session["score"] = score
            session["displayed_question"] = questions.pop() # last question
            print(session["displayed_question"])
            session["count"] = count + 1
            return render_template('question.html', question = session["displayed_question"],id = id,button="Submit")
        except:
            #question.pop returns an error
            return render_template('results.html', level=level, score=score)

@app.route('/results',methods=['GET','POST'])
def results():
    time=''
    if request.method == "POST":
        time=request.form.get('data')
        score = session.get("score", 0)
        id = session.get('id')
        print(id)

        t = str(timedelta(seconds=int(time)))
        print('time is',t[2:])
        #print('score is',time)

        #update the database
        conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('''UPDATE PLAYERS SET score = ? , time = ? WHERE id= ?''', (score, t[2:], id))
        conn.commit()
        c.close()
    return time


if __name__ == "__main__":
    app.run(debug=True)