
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
from database.config import db
from utils.validator import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)
app.config['MYSQL_DATABASE_HOST'] = db['host']
app.config['MYSQL_DATABASE_USER'] = db['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['password']
app.config['MYSQL_DATABASE_DB'] = db['name']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize database variables..
mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cur = conn.cursor()

# Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username

    # def get_id(self):
    #     return (self.user_id)


@app.route('/error')
@login_required
def error():
    try:
        if session['ERROR_EXISTS']:
            return render_template('error.html')
    except:
        return redirect(url_for('dashboard', username=session['username']))


@app.route('/')
def index():
    if User.is_authenticated:
        return redirect(url_for('dashboard',
                                user=session))
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
        # Here, we reinitialize it, and execute the query.
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(q.format(username))
            match = cur.fetchone()
        except:
            # [Done] Redirect to a separate route meant for errors.
            session['ERROR_EXISTS'] = True
            return redirect(url_for('error'))

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
    session['logged_in'] = True
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
        cur.execute(q.format(username))
        match = cur.fetchone()
    except:
        # Connection-Reset-On-Idle exception handler.
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(q.format(username))
            match = cur.fetchone()
        except:
            # [Done] Redirect to a separate route meant for errors.
            session['ERROR_EXISTS'] = True
            return redirect(url_for('error'))

    if match is not None:
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
        session['ERROR_EXISTS'] = True
        return redirect(url_for('error'))

    # Log the user in.
    login_user(User(username))
    session['logged_in'] = True
    session['name'] = name
    session['username'] = username
    return redirect(url_for('dashboard', username=username))


# PROFILE ROUTE

@app.route("/<string:username>")
def view_profile(username):
    # Check if user is logged in, to avoid a database query.
    if User.is_authenticated:
        if username == session['username']:
            return render_template('profile.html', user=session)

    # When user is not logged in, query the DB and fetch info.
    # SELECTing only `name` for now. SELECT more items later as DB grows,
    # and that too from a different table.
    q = "SELECT `name` FROM `credentials` WHERE username='{}';"
    try:
        cur.execute(q.format(username))
        profile_data = cur.fetchall()
    except:
        # Try from scratch if connection fails.
        try:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(q.format(username))
            profile_data = cur.fetchall()
        except:
            session['ERROR_EXISTS'] = True
            return redirect(url_for('error'))

    # Now, everything needed to view profile is in `profile_data`.
    # Proceeding to view profile.
    return render_template('profile.html',
                           person=profile_data)


@app.route('/public/articles')
def public_feed():
    q = """
    SELECT credentials.username AS author,posts.title,posts.body,posts.likes
    FROM `posts`
    INNER JOIN `credentials`
    ON posts.author_uid = credentials.user_id;
    """
    cur.execute(q)
    rows = cur.fetchall()
    """
    Using `fetchall` for simplicity.
    `fetchmany(size=)` to be used for limited posts.
    Unloaded posts will be loaded via an AJAX request,
    in a later version.
    """
    # Above statement fetches records in tuple form.
    # Changing to dictionary format.
    posts = []
    fields = [x[0] for x in cur.description]

    for row in rows:
        post = {}
        for i in range(len(fields)):
            post[fields[i]] = row[i]
        posts.append(post)

    return render_template('public-feed.html',
                           title='Public Feed',
                           user=session,
                           posts=posts)


# PROTECTED ROUTES


@app.route('/<string:username>/dashboard')
@login_required
def dashboard(username):
    if username == session['username']:
        # Open dashboard of only the logged in user, and not of someone else.
        return render_template('dashboard.html', user=session)
    # If a logged-in user tries to open dashboard of someone else, redirect to
    # his own dashboard, LOL :)
    return redirect('/{user}/dashboard'.format(user=session['username']))


@app.route('/new')
@login_required
def new():
    return render_template('add-new-article.html', user=session)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html',
                           msg='You have been logged out')


if __name__ == '__main__':
    # In dev mode:
    app.run(debug=True)
