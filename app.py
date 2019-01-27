# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, render_template, g, abort, request, flash, redirect, url_for, session
from forms import LoginForm, UserRegisterForm
import datetime
import hashlib
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'reeeeeee'

DATABASE = 'database.db'

class Wniosek:
    OCZEKUJACY = 0
    ZAAKCEPTOWANY = 1
    ODRZUCONY = 2


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('files', path)

@app.route('/login', methods=['GET'])
def login_form():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    user = form.username.data
    password = form.password.data

    salt = query_db('select salt from Osoba where email = ?', [user], one=True)
    if not salt:
        flash("nie ma takiego uzytkownika")
        return redirect(url_for('login_form'))

    hash = hashlib.sha256(password + salt[0]).hexdigest()
    user_email = query_db('select email from Osoba where email = ? and password = ?', [user, hash], one=True)
    if not user:
        flash("bledne haslo")
        return redirect(url_for('login_form'))

    flash("witaj {name}".format(name=user_email[0]))

    userType = ''
    player = query_db('select 1 from Zawodnik where email = ?', [user])
    if player:
        userType = 'player'
    referee = query_db('select 1 from Sedzia where email = ?', [user])
    if referee:
        userType = 'referee'
    admin = query_db('select 1 from ZarzadcaLigi where email = ?', [user])
    if admin:
        userType = 'admin'
    coach = query_db('select 1 from Trener where email = ?', [user])
    if coach:
        userType = 'coach'

    session['username'] = user_email[0]
    session['type'] = userType
    return redirect(url_for('index'))

@app.route('/register/<person>', methods=['GET'])
def register_form(person):
    if person not in ['player', 'referee', 'admin', 'coach']:
        return abort(404)

    welcome_texts = { 'player':'zawodnik', 'referee': u'sędzia', 'admin': u'zarządca ligi', 'coach': u'trener'}
    p = welcome_texts[person]
    form = UserRegisterForm()
    return render_template('register.html', person=person, form=form, welcome=p)

@app.route('/register/<person>', methods=['POST'])
def register(person):
    form = UserRegisterForm()
    name = form.name.data
    surname = form.surname.data
    username = form.username.data
    password = form.password.data

    db = get_db()
    cur = db.execute('SELECT * FROM Osoba WHERE email = ?', [username])
    if cur.fetchone():
        flash("uzytkownik z tym emailem juz istnieje")
        return redirect(url_for('register', person=person))

    salt = os.urandom(4).encode('hex')
    hash = hashlib.sha256(password + salt).hexdigest()

    db.execute('insert into Osoba values (?, ?, ?, ?, ?);', [name, surname, username, salt, hash])
    
    table_map = {'player':'Zawodnik', 'referee':'Sedzia', 'admin':'ZarzadcaLigi', 'coach':'Trener'}
    table_name = table_map[person]

    db.execute('insert into {table} (\'email\') values (?)'.format(table=table_name), [username])
    db.commit()
    return redirect(url_for('login_form'))

@app.route('/addteam', methods=['GET'])
def add_team():
    if session.get('type') != 'coach':
        flash(u"brak uprawnień")
        return redirect(url_for('index'))

    t = query_db('select nazwa, logo FROM Druzyna WHERE trener = ?', [session.get('username')])
    if not t:
        flash(u"trener nie posiada żadnej drużyny przypisanej do niego")
        return redirect(url_for('index'))

    team_name, team_logo = t[0]
    players = query_db('SELECT z.numer, o.imie, o.nazwisko FROM Zawodnik z JOIN Osoba o ON z.email=o.email WHERE druzyna = ?', [team_name])
    return render_template('add_team.html', team_name=team_name, players=players)

@app.route('/addteam', methods=['POST'])
def create_team():
    if session.get('type') != 'coach':
        flash(u"brak uprawnień")
        return redirect(url_for('index'))

    t = query_db('select nazwa, logo FROM Druzyna WHERE trener = ?', [session.get('username')])
    if not t:
        flash(u"trener nie posiada żadnej drużyny przypisanej do niego")
        return redirect(url_for('index'))

    team_name, team_logo = t[0]
    teamTable = request.json['teamTable']
    reserveTable = request.json['reserveTable']

    db = get_db()
    db.execute('INSERT INTO Sklad (\'trener\') VALUES (?)', [session['username']])
    cur = db.execute('select seq from sqlite_sequence where name=\'Sklad\'')
    skladId = int(cur.fetchone()[0])

    for player in teamTable:
        number, name, surname = player
        player_email = query_db('SELECT email FROM Zawodnik WHERE druzyna=? AND numer=?;', [team_name, number], one=True)[0]
        print(skladId, player_email)
        db.execute('INSERT INTO TworzySklad VALUES (?, ?, ?);', [skladId, player_email, 0])
    
    for player in reserveTable:
        number, name, surname = player
        player_email = query_db('SELECT email FROM Zawodnik WHERE druzyna=? AND numer=?;', [team_name, number], one=True)[0]
        db.execute('INSERT INTO TworzySklad VALUES (?, ?, ?);', [skladId, player_email, 1])

    db.execute('''INSERT INTO Wniosek ('data', 'status', 'zglaszajacy') VALUES (?, ?, ?);''',
                [str(datetime.datetime.now()), Wniosek.OCZEKUJACY, session.get('username')])
    cur = db.execute('''select seq from sqlite_sequence where name='Wniosek';''')
    wniosekId = int(cur.fetchone()[0])

    db.execute('''INSERT INTO WniosekSkladowy VALUES (?, ?);''', [wniosekId, skladId])
    db.commit()

    flash(u"Twój wniosek został zapisany")
    return 'OK'

@app.route('/forms', methods=['GET'])
def show_forms():
    if session.get('type') != 'admin':
        flash(u"brak uprawnień")
        return redirect(url_for('index'))

    forms = query_db('''SELECT Dr.nazwa, Dr.logo, W.data, W.zglaszajacy, W.id
        FROM WniosekDruzynowy D
        JOIN Wniosek W ON W.id=D.WniosekId
        JOIN Druzyna Dr ON Dr.trener=W.zglaszajacy
        WHERE W.status=0''')
    player_lists = []

    teams = []
    for f in forms:
        name, logo, date, coach, id = f

        players = query_db('''SELECT O.imie, O.nazwisko, Z.numer
        FROM Osoba O
        JOIN Zawodnik Z ON O.email=Z.email
        JOIN Druzyna D ON Z.druzyna=D.nazwa
        WHERE D.trener = ?''', [coach])

        t = {
            'id': id,
            'name': name,
            'logo': logo,
            'date': date,
            'coach': coach,
            'players': players
        }
        teams.append(t)
    return render_template('show_forms.html', teams=teams)

@app.route('/forms', methods=['POST'])
def add_form():
    accepted = request.form.get('accepted') == 'true'
    reason = request.form.get('reason')
    id = request.form.get('id')

    form_status = {True:1, False:2}[accepted]

    if accepted:
        flash("zatwierdzono wniosek")
    else:
        flash("odrzucono wniosek")

    db = get_db()
    db.execute('''UPDATE Wniosek SET status=?, uwagi=?, rozpatrujacy=? WHERE id=?''', [form_status, reason, session.get('username'), id])
    db.commit()

    return redirect(url_for('show_forms'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset_db():
    db = get_db()
    cur = db.cursor()
    script = open('reset.sql', 'rb').read()
    cur.executescript(script)
    db.commit()
    cur.close()
    db.close()
    return 'reset OK!'


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)
