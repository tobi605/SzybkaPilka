from flask import Flask, send_from_directory, render_template, g, abort, request, flash, redirect, url_for, session
from datetime import datetime
from forms import LoginForm, UserRegisterForm
import hashlib
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'reeeeeee'

import os

DATABASE = 'database.db'

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
    user = query_db('select imie from Osoba where email = ? and password = ?', [user, hash], one=True)
    if not user:
        flash("bledne haslo")
        return redirect(url_for('login_form'))

    flash("witaj {name}".format(name=user[0]))
    session['username'] = user[0]
    return redirect(url_for('index'))

@app.route('/register/<person>', methods=['GET'])
def register_form(person):
    if person not in ['player', 'referee', 'admin']:
        return abort(404)

    form = UserRegisterForm()
    return render_template('register.html', person=person, form=form)

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
    
    table_map = {'player':'Zawodnik', 'referee':'Sedzia', 'admin':'ZarzadcaLigi'}
    table_name = table_map[person]

    db.execute('insert into {table} (\'email\') values (?)'.format(table=table_name), [username])

    db.commit()
    return redirect(url_for('login_form'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)