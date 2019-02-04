#! /usr/bin/python3

from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, username):
        self.uid = username


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/signin')
@app.route('/login')
def login():
    return render_template('login.html',
                           title='Log In')


@app.route('/signup')
@app.route('/join')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    # In dev mode:
    app.run(debug=True)
