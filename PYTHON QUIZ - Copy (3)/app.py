from flask import Flask, render_template, request, redirect, session, url_for
import smtplib
from datetime import datetime
import sqlite3
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-string'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    option = request.form.get('radio')
    print(option)
    session['lvl'] = option
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
    c.execute('SELECT id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse FROM QUESTIONS')
    questions = c.fetchall()

    if level=='easy':
        mylist = [i for i in range(1,21)]

    if level=='medium':
        mylist = [i for i in range(21,41)]

    if level=='hard':
        mylist = [i for i in range(41,61)]
        
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
    return redirect(url_for('questions', id=ids.pop()))

@app.route('/questions/<id>')
def questions(id):
    print("ROUTE /quiz", id)

    # ανάκτησε από το session την κατάσταση...
    score = session.get("score", 0)
    count = session.get("count",0)
    level = session.get("difficulty")
    questions = session.get("questions", []) #random questions
    displayed_question = session.get("displayed_question", [])

    if request.query_string: # ο χρήστης απάντησε
        reply = request.args.get("answer")
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
            # read time and update database
            #storage= window.localStorage
            time = request.args.get("timetag")
            print(time)
            return render_template('results.html', level=level, score=score)

@app.route('/results')
def results():
    if request.query_string: # ο χρήστης απάντησε
        score = request.args.get("score")
        print("score is:",score)
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)