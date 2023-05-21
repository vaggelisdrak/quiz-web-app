from flask import Flask, render_template, request, redirect, session, url_for 
import smtplib
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import random
import sqlite3
import os

app = Flask(__name__)
#app.secret_key = 'hard-to-guess-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.secret_key = os.environ.get('SECRET')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PLAYERS.db'

ENV = 'prod' 

if ENV == 'dev':
    app.debug = True
    app.secret_key = 'hard-to-guess-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PLAYERS.db'
else:
    app.debug = False
    app.secret_key = os.environ.get('SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#initialize the database
db = SQLAlchemy(app)

#create db model
class Players(db.Model):
    name = db.Column(db.String(200), nullable=False)#you can t enter a null name
    email = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    #name TEXT, email TEXT, level TEXT, score INT, date TEXT, time TEXT,points INT, id INTEGER PRIMARY KEY AUTOINCREMENT)'
    #create a function to return a sting when we add something
    def __repr__(self):
        return "<Name %r>" % self.id


@app.route('/')
def index():
    return render_template("index.html")#home page

@app.route('/login')
def login():
    try:
        if session['first_name'] and session['email']:#remember the previous login
            first_name = session['first_name']
            email = session['email']
            return render_template("login.html",first_name=first_name,email=email)
    except:
        return render_template("login.html")

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get('first_name')
    email = request.form.get('email')
    option = request.form.get('radio')
    print(option)

    #initialize 
    session['first_name'] = first_name 
    session['email'] = email
    session['lvl'] = option
    score = 0 
    points = 0
    now = datetime.now()
    dt= now.strftime("%d/%m/%Y %H:%M:%S")# dd/mm/YY H:M:S
    time = '00:00'

    #connect to the database and check if the username already exists and if the email matches it
    #conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
    #c = conn.cursor()
    #c.execute('SELECT name,email FROM PLAYERS')
    #users = c.fetchall()
    users = []
    games = Players.query.all()
    for g in games:
        users.append((g.name,g.email))

    if not users:#if it is the first player
        pass
    else:
        for n,e in users:
            if n==first_name and e!=email:
                error = ' This username already exists or the email is incorrect!'
                return render_template('login.html',first_name=first_name,email=email,error=error)

    #append the game,player to the database
    #c.execute("INSERT INTO PLAYERS(name, email, level, score, date, time, points) VALUES (?, ?, ?, ?, ?, ?, ?)",(first_name, email, option, score, dt, time, points))
    #print('last_row_id: ',c.lastrowid)
    #session['id'] = c.lastrowid
    new_game = Players(name=first_name, email =email, level = option, score = score, date = dt, time = time, points = points)
    db.session.add(new_game)
    db.session.commit()
    session['id'] = new_game.id
    print("id is: ",session['id'])
    #load all the games this player has played
    #c.execute('SELECT name,email,level,score,date,time,points FROM PLAYERS')
    #players = c.fetchall()
    players = []
    allgames = Players.query.all()
    for g in allgames:
        players.append((g.name,g.email,g.level,g.score,g.date,g.time,g.points))

    player = []
    games_played=0
    for n,e,l,s,d,t,p in players[:-1]:
        if n==first_name and e==email:
            games_played+=1
            player.append((n,e,l,s,d,t,p))

    player.reverse()#the most recent appear first
    #conn.commit()

    #leaderboard
    topplayers = [] 
    for pl in players:
        time = int(pl[5][0])*10*60 + int(pl[5][1])*60 + int(pl[5][3])*10 + int(pl[5][4])
        if time>3:
            p = (pl[3])*10 + int(100/time)
        else:
            p = 0   
        topplayers.append((pl[0],pl[1],pl[2],p))

    bestplayers = []
    for i in sorted(topplayers,key=lambda tup: tup[3],reverse=True):
        bestplayers.append(i)

    best_easy=[]
    best_medium=[]
    best_hard=[]
    for j in bestplayers:
        if j[2]=='easy':
            best_easy.append(j)
        if j[2]=='medium':
            best_medium.append(j)
        if j[2]=='hard':
            best_hard.append(j)

    print(len(best_easy))
    print(len(best_medium))
    print(len(best_hard))

    #player's best games for each level and his rank
    easy_rank=0
    easy_best_game_points = 0
    for g in best_easy:
        easy_rank+=1
        if g[0]==first_name and g[1]==email:
            easy_best_game_points = g[3]
            break

    medium_rank=0
    medium_best_game_points = 0
    for g in best_medium:
        medium_rank+=1
        if g[0]==first_name and g[1]==email:
            medium_best_game_points = g[3]
            break

    hard_rank=0
    hard_best_game_points = 0
    for g in best_hard:
        hard_rank+=1
        if g[0]==first_name and g[1]==email:
            hard_best_game_points = g[3]
            break

    print(easy_rank,easy_best_game_points)
    print(medium_rank,medium_best_game_points)
    print(hard_rank,hard_best_game_points)

    #initialize the podium if less than 3 games exist for each level
    if len(best_easy)<3:
        for i in range(3):
            best_easy.append(('','','easy',''))

    if len(best_medium)<3:
        for i in range(3):
            best_medium.append(('','','medium',''))

    if len(best_hard)<3:
        for i in range(3):
            best_hard.append(('','','hard',''))
    
    print(best_easy)
    print(best_medium)
    print(best_hard)
    #conn.close()

    if not player:#if it is a new player
        return redirect(url_for("start"))
    else:
        print(player[0])
        return render_template("form.html",player=player,games=games_played,level=option,last_level=player[0][2],
        best_easy=best_easy,best_medium=best_medium,best_hard=best_hard,#best games for each level
        easy_rank=easy_rank,#player's best game rank   / easy
        medium_rank=medium_rank,#player's best game rank  / medium
        hard_rank=hard_rank,#player's best game rank  / hard
        total_easy=len(best_easy),#total games  /easy
        total_medium=len(best_medium),#total games  /medium
        total_hard=len(best_hard))#total games  /hard


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
    level = session.get("lvl") # get from the session
    conn = sqlite3.connect('QUESTIONS.db', check_same_thread=False)
    c = conn.cursor()

    #initialize the questions
    random_questions = []
    options = []
    ids =[]
    mylist = []

    #select random questions based on the level of difficulty 
    c.execute('SELECT id, level, question, ans1, ans2, ans3, ans4, correctans, explanation, reccourse FROM QUESTIONS')
    questions = c.fetchall()

    if level=='easy':
        for i in range(1,21):
            mylist.append(i)

    if level=='medium':
        for i in range(21,41):
            mylist.append(i)

    if level=='hard':
        for i in range(41,61):
            mylist.append(i)
        
    print(mylist)
    x = random.sample(mylist,5)#5 random questions
    print(x)
    for i,l,q,a1,a2,a3,a4,c,ex,re in questions:
        if i in x:
            random_questions.append((i,l,q,a1,a2,a3,a4,c,ex,re))
            options.append((a1,a2,a3,a4))
            ids.append(i)
    conn.close()

    print(ids)#questions' id
    print(random_questions)

    #initialize the session for the questions and the results
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

    #get from the session
    score = session.get("score", 0)
    count = session.get("count",0)
    level = session.get("difficulty")
    questions = session.get("questions", [])#all random questions

    if request.query_string: #if the user replies
        reply = request.args.get("answer") #player's answer
        correct = session["displayed_question"][7] #correct answer
        print(reply,correct)
        new_score = 0
        if reply == correct:
            new_score=1
        score += new_score
        print('score is...', score)
        #print(questions)
        if questions: 
            next_question = questions[-1]# the next question is the last one from the list
        else:
            next_question = "end"#if there are not any questions 
        session["score"] = score

        # react to his answer
        return render_template('question.html', question = session["displayed_question"],
            id = id, next_question = next_question, button="Next",
            disabled = "disabled",correct=correct,reply=reply)

    else: # send the question to the user
        try:
            session["score"] = score
            session["displayed_question"] = questions.pop() #choose from th list the last question
            print(session["displayed_question"])
            session["count"] = count + 1
            return render_template('question.html', question = session["displayed_question"],id = id,button="Submit")
        except:
            #question.pop returns an error because there aren't any questions 
            return render_template('results.html', level=level, score=score)

@app.route('/results',methods=['GET','POST'])# jquery ajax method sends a request to the server (so data can be transfered from js to python)
def results():
    time=''
    if request.method == "POST":
        #get the results
        time=request.form.get('data')
        score = session.get("score", 0)
        id = session.get('id')
        print(id)

        t = str(timedelta(seconds=int(time)))
        print('time is',t[2:])

        p = int(score)*10 + int(100/int(time))
        print(p)
        #print('score is',time)

        #update the database
        #conn = sqlite3.connect('PLAYERS.db', check_same_thread=False)
        #c = conn.cursor()
        #c.execute('''UPDATE PLAYERS SET score = ? , time = ?, points = ? WHERE id= ?''', (score, t[2:], p , id))
        #conn.commit()
        #c.close()
        game_to_update = Players.query.get_or_404(id)
        game_to_update.score = score
        game_to_update.time = t[2:]
        game_to_update.points = p
        db.session.commit()
    return time


if __name__ == "__main__":
    #db.create_all()
    app.run()