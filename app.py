# -*- coding: utf-8 -*-
"""
    backend
"""
import datetime
import hashlib
import sqlite3
import os

from flask import Flask, send_from_directory, render_template, g, abort, \
    request, flash, redirect, url_for, session
from forms import LoginForm, UserRegisterForm

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'supersecretpassword'

DATABASE = 'database.db'

WNIOSEK_ID = {
    'OCZEKUJACY': 0,
    'ZAAKCEPTOWANY': 1,
    'ODRZUCONY': 2,
}


def get_db():
    """
        get db connector
    """
    db_link = getattr(g, '_database', None)
    if db_link is None:
        db_link = g._database = sqlite3.connect(DATABASE)
    return db_link

def query_db(query, args=(), one=False):
    """
        execute a query and return rows
    """
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows

@APP.teardown_appcontext
def close_connection(_):
    """
        close database on exit
    """
    db_link = getattr(g, '_database', None)
    if db_link is not None:
        db_link.close()

@APP.route('/static/<path:path>')
def send_static(path):
    """
        send files from static dir
    """
    return send_from_directory('files', path)

@APP.route('/login', methods=['GET'])
def login_form():
    """
        send login form
    """
    form = LoginForm()
    return render_template('login.html', form=form)

@APP.route('/login', methods=['POST'])
def login():
    """
        login user
    """
    form = LoginForm()
    user = form.username.data
    password = form.password.data

    salt = query_db('select salt from Osoba where email = ?', [user], one=True)
    if not salt:
        flash("nie ma takiego uzytkownika")
        return redirect(url_for('login_form'))

    pass_hash = hashlib.sha256(password + salt[0]).hexdigest()
    user_email = query_db('select email from Osoba where email = ? and password = ?',
                          [user, pass_hash], one=True)
    if not user_email:
        flash("bledne haslo")
        return redirect(url_for('login_form'))

    flash("witaj {name}".format(name=user_email[0]))

    user_type = ''
    player = query_db('select 1 from Zawodnik where email = ?', [user])
    if player:
        user_type = 'player'
    referee = query_db('select 1 from Sedzia where email = ?', [user])
    if referee:
        user_type = 'referee'
    admin = query_db('select 1 from ZarzadcaLigi where email = ?', [user])
    if admin:
        user_type = 'admin'
    coach = query_db('select 1 from Trener where email = ?', [user])
    if coach:
        user_type = 'coach'

    session['username'] = user_email[0]
    session['type'] = user_type
    return redirect(url_for('index'))

@APP.route('/register/<person>', methods=['GET'])
def register_form(person):
    """
        send user register form
    """
    if person not in ['player', 'referee', 'admin', 'coach']:
        return abort(404)

    welcome_texts = {'player':'zawodnik', 'referee': u'sędzia',
                     'admin': u'zarządca ligi', 'coach': u'trener'}
    p_text = welcome_texts[person]
    form = UserRegisterForm()
    return render_template('register.html', person=person, form=form, welcome=p_text)

@APP.route('/register/<person>', methods=['POST'])
def register(person):
    """
        register specified user
    """
    form = UserRegisterForm()
    name = form.name.data
    surname = form.surname.data
    username = form.username.data
    password = form.password.data

    db_link = get_db()
    cur = db_link.execute('SELECT * FROM Osoba WHERE email = ?', [username])
    if cur.fetchone():
        flash("uzytkownik z tym emailem juz istnieje")
        return redirect(url_for('register', person=person))

    salt = os.urandom(4).encode('hex')
    pass_hash = hashlib.sha256(password + salt).hexdigest()

    db_link.execute('insert into Osoba values (?, ?, ?, ?, ?);',
                    [name, surname, username, salt, pass_hash])

    table_map = {'player':'Zawodnik', 'referee':'Sedzia', 'admin':'ZarzadcaLigi', 'coach':'Trener'}
    table_name = table_map[person]

    db_link.execute('insert into {table} (\'email\') values (?)'
                    .format(table=table_name), [username])
    db_link.commit()
    return redirect(url_for('login_form'))

@APP.route('/addteam', methods=['GET'])
def add_team():
    """
        show form for adding a team
    """
    if session.get('type') != 'coach':
        flash(u"brak uprawnień")
        return redirect(url_for('index'))

    coach = query_db('select nazwa, logo FROM Druzyna WHERE trener = ?', [session.get('username')])
    if not coach:
        flash(u"trener nie posiada żadnej drużyny przypisanej do niego")
        return redirect(url_for('index'))

    team_name, _ = coach[0]
    players = query_db('SELECT z.numer, o.imie, o.nazwisko FROM Zawodnik z \
                        JOIN Osoba o ON z.email=o.email WHERE druzyna = ?', [team_name])
    return render_template('add_team.html', team_name=team_name, players=players)

@APP.route('/addteam', methods=['POST'])
def create_team():
    """
        push team to db
    """
    if session.get('type') != 'coach':
        return abort(403)

    rows = query_db('select nazwa, logo FROM Druzyna WHERE trener = ?', [session.get('username')])
    if not rows:
        flash(u"trener nie posiada żadnej drużyny przypisanej do niego")
        return redirect(url_for('index'))

    team_name, _ = rows[0]
    team_table = request.json['teamTable']
    reserve_table = request.json['reserveTable']

    db_link = get_db()
    db_link.execute('INSERT INTO Sklad (\'trener\') VALUES (?)', [session['username']])
    cur = db_link.execute('select seq from sqlite_sequence where name=\'Sklad\'')
    sklad_id = int(cur.fetchone()[0])

    for player in team_table:
        number, _, _ = player
        player_email = query_db('SELECT email FROM Zawodnik WHERE druzyna=? AND numer=?;',
                                [team_name, number], one=True)[0]
        db_link.execute('INSERT INTO TworzySklad VALUES (?, ?, ?);', [sklad_id, player_email, 0])

    for player in reserve_table:
        number, _, _ = player
        player_email = query_db('SELECT email FROM Zawodnik WHERE druzyna=? AND numer=?;',
                                [team_name, number], one=True)[0]
        db_link.execute('INSERT INTO TworzySklad VALUES (?, ?, ?);', [sklad_id, player_email, 1])

    db_link.execute('''INSERT INTO Wniosek ('data', 'status', 'zglaszajacy') VALUES (?, ?, ?);''',
                    [str(datetime.datetime.now()), WNIOSEK_ID['OCZEKUJACY'],
                     session.get('username')])
    cur = db_link.execute('''select seq from sqlite_sequence where name='Wniosek';''')
    wniosek_id = int(cur.fetchone()[0])

    db_link.execute('''INSERT INTO WniosekSkladowy VALUES (?, ?);''', [wniosek_id, sklad_id])
    db_link.commit()

    flash(u"Twój wniosek został zapisany")
    return 'OK'

@APP.route('/forms', methods=['GET'])
def show_forms():
    """
        show forms for accepting forms
    """
    if session.get('type') != 'admin':
        flash(u"brak uprawnień")
        return redirect(url_for('index'))

    forms = query_db('''SELECT Dr.nazwa, Dr.logo, W.data, W.zglaszajacy, W.id
        FROM WniosekDruzynowy D
        JOIN Wniosek W ON W.id=D.WniosekId
        JOIN Druzyna Dr ON Dr.trener=W.zglaszajacy
        WHERE W.status=0''')

    teams = []
    for form in forms:
        name, logo, date, coach, form_id = form

        players = query_db('''SELECT O.imie, O.nazwisko, Z.numer
        FROM Osoba O
        JOIN Zawodnik Z ON O.email=Z.email
        JOIN Druzyna D ON Z.druzyna=D.nazwa
        WHERE D.trener = ?''', [coach])

        team = {
            'id': form_id,
            'name': name,
            'logo': logo,
            'date': date,
            'coach': coach,
            'players': players
        }
        teams.append(team)
    return render_template('show_forms.html', teams=teams)

@APP.route('/forms', methods=['POST'])
def add_form():
    """
        set form as processed in db
    """
    accepted = request.form.get('accepted', None) == 'true'
    reason = request.form.get('reason', None)
    form_id = request.form.get('id', None)

    if 'username' not in session or session.get('type') != 'admin':
        return abort(403)

    if accepted is None or reason is None or form_id is None:
        return abort(500)

    form_status = {True:1, False:2}[accepted]

    db_link = get_db()
    db_link.execute('''UPDATE Wniosek SET status=?, uwagi=?, rozpatrujacy=? WHERE id=?''',
                    [form_status, reason, session.get('username'), form_id])
    db_link.commit()

    if accepted:
        flash("zatwierdzono wniosek")
    else:
        flash("odrzucono wniosek")

    return 'OK'

@APP.route('/')
def index():
    """
        return index site
    """
    return render_template('index.html')

@APP.route('/reset')
def reset_db():
    """
        reset database to original setup
    """
    db_link = get_db()
    cur = db_link.cursor()
    script = open('reset.sql', 'rb').read()
    cur.executescript(script)
    db_link.commit()
    cur.close()
    db_link.close()
    return 'reset OK!'


if __name__ == '__main__':
    APP.run(debug=False, use_reloader=True)
