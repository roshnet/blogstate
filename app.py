#! /usr/bin/python3

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flaskext.mysql import MySQL
from dbconfig.config import db
from utils.validator import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)
app.config['MYSQL_DATABASE_HOST'] = db['host']
app.config['MYSQL_DATABASE_USER'] = db['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['password']
app.config['MYSQL_DATABASE_DB'] = db['name']

# Initialize database variables..
mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cur = conn.cursor()

# Initialize flask-login..
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username

    # def get_id(self):
    #     return (self.user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',
                               title='Log In')

    # [Do] Process login instead.
    username = request.form['username']
    passwd = request.form['passwd']

    # Assuming clean data, proceeding.
    q = "SELECT `hash`, `name` FROM `credentials` WHERE username='{}';"
    try:
        cur.execute(q.format(username))
        match = cur.fetchone()
    except:
        # Exception handler for 500 Internal Server Error.
        # Being idle for too long (before login) forgets the DB connection.
        # Here, we reintialize it, and execute the query.
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(q.format(username))
            match = cur.fetchone()
        except:
            # [Later] Redirect to a separate template meant for errors.
            error = '''
            <h1>Something unfortunately broke :( </h1>
            <h3>Click <a href="{{ url_for('login') }}">here</a>
            to return to login page.</h3>
            Error Description: {}
            '''
            return error

    if match is None:
        return render_template('login.html',
                               issue='Username or password is incorrect')

    # If username exists, proceed to compare passwords.
    hashed = match[0]
    if not check_password_hash(hashed, passwd):
        return render_template('login.html',
                               issue='Username or password is incorrect')

    # Else, log the user in.
    login_user(User(username))
    session['name'] = match[1]
    session['username'] = username
    return redirect(url_for('dashboard',
                            username=username))


@app.route('/signup')
@app.route('/join', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # [Do] Process data instead..
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    passwd = request.form['passwd']

    # [WIP] Check for sanity of fields, redirect if unclean (avoid SQLIA).
    resp = validate(username, name)
    if resp['is_valid'] == 0:
        return render_template('signup.html',
                               issue=resp['message'])
    elif resp['is_valid'] == 1:
        name = resp['name']

    # [Do] Check for username availability (assuming clean data)
    q = "SELECT `name` FROM `credentials` WHERE username='{}';"
    try:
        cur.execute(q)
        match = cur.fetchone()
    except:
        # Connection-Reset-On-Idle exception handler.
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(q.format(username))
            match = cur.fetchone()
        except:
            # [Later] Redirect to a separate template meant for errors.
            error = '''
            <h1>Something unfortunately broke :( </h1>
            <h3>Click <a href="{{ url_for('signup') }}">here</a>
            to return to signup page.</h3>
            Error Description: {}
            '''
            return error

    if not match is None:
        return render_template('signup.html',
                               issue='Username already taken')

    # Proceed with insertion otherwise.
    q = '''
    INSERT INTO `credentials` (username, name, hash, email) 
    VALUES (%s,%s,%s,%s)
    '''

    try:
        cur.execute(q, (username,
                        name,
                        generate_password_hash(passwd, method='sha1'),
                        email))
        conn.commit()

    except:
        error = '''
        Something bad happened :(
        <h3>Click <a href="{{ url_for('signup') }}">here</a>
        to return to signup page.</h3>
        Error Description: {}
        '''
        return error

    # Log the user in.
    login_user(User(username))
    session['name'] = name
    session['username'] = username
    return redirect(url_for('dashboard', username=username))



# PROTECTED ROUTES


@app.route("/<string:username>")
@login_required
def dashboard(username):
    return render_template('dashboard.html', user=session)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html',
                           msg='You have been logged out')


if __name__ == '__main__':
    # In dev mode:
    app.run(debug=True)
