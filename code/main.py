import logging
import recommender

#try:
# from google.appengine.ext import vendor
# vendor.add('lib')
#except ImportError:
#    logging.warning('google app engine unable to be imported')

from flask import Flask, render_template, redirect, url_for, request, make_response
app = Flask(__name__)

# === Configure sass for app
from flask_scss import Scss
Scss(app, static_dir='code/static', asset_dir='code/static')

# === APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'secretkey123984392032'

import os
import MySQLdb
from user_class import User
from surveys import UserInterests
from event import Event, EventForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

# CLOUDSQL_CONNECTION_NAME = "gennyc-dev:us-central1:mysqldev"
# CLOUDSQL_USER = "kayvon"
# CLOUDSQL_PASSWORD = "kayvon"

# DB_HOST_DEV = '35.193.223.145'
DB_HOST_DEV = "127.0.0.1"

# ENV = ''
# if os.environ.get('BRANCH') != 'master':
#     ENV = 'Dev'
# else:
#     ENV = 'Uat'
#     CLOUDSQL_CONNECTION_NAME = 'gennyc-uat:us-central1:mysqluat'
#


ENV_DB = 'Dev'
# print (os.environ.get('BRANCH'))

MOCK_EVENTS = [Event('Rollerblading Tour of Central Park', 2018, 3, 20, 'Join this fun NYC tour and get some exercise!'),
                Event('Rollerblading Tour of Central Park Round 2', 2018, 3, 22, 'Join this fun NYC tour and get some exercise again!')]


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    else:
        db = MySQLdb.connect(
            host=DB_HOST_DEV, user='kayvon', passwd='kayvon', db='Dev', port=3306)

    return db

# def auth_user_mock(user: User) -> bool:
#     return user in MOCK_USERS


def query_for_user(user):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM " + ENV_DB + ".Users WHERE username='" + user.username + "'")
    data = cursor.fetchone()
    db.close()
    return data


def authenticate_user(user):
    result = query_for_user(user)
    if result is None:
        return False
    elif result[2] == user.password:
        return True
    return False

@login_manager.user_loader
def load_user(user_name):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("SELECT username, password, email, fname, lname, dob, timezone FROM " + ENV_DB + ".Users WHERE username='" + user_name + "'")
    data = cursor.fetchone()
    db.close()
    if data is None:
        return None
    return User(*data)


def insert_new_user(user):
    db = connect_to_cloudsql()
    cursor = db.cursor()

    query = "INSERT INTO "+ ENV_DB + ".Users(username, password, fname, lname, dob, date_joined, timezone, email) VALUES('{}', '{}', {}, {}, {}, {}, {}, {})".format(
            user.username,
            user.password,
            "'" + user.fname + "'" if user.fname else 'NULL',
            "'" + user.lname + "'" if user.lname else 'NULL',
            "'" + user.dob + "'" if user.dob else 'NULL',
            "'" + str(user.join_date) + "'" if user.join_date else 'NULL',
            "'" + user.timezone + "'" if user.timezone else 'NULL',
            "'" + user.email + "'" if user.email else 'NULL')

    cursor.execute(query)
    db.commit()
    db.close()


def register_user(user):
    if query_for_user(user):
        return False

    insert_new_user(user)
    if query_for_user(user):
        return True


@app.route('/')
def index():
    return render_template("hello.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        try:
            new_user = User(request.form['username'],
                            request.form['password'],
                            request.form['email'],
                            request.form['fname'],
                            request.form['lname'],
                            request.form['dob'],
                            request.form['timezone']
                            )
        except ValueError:
            error = 'Username or Password is empty.'

        if (register_user(new_user)):
            login_user(new_user)
            return redirect(url_for('home'))
        else:
            error = 'Username taken.'

    return render_template('register.html', error = error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        test_user = User(request.form['username'], request.form['password'])

        if authenticate_user(test_user):
            login_user(test_user)
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/home')
@login_required
def home():
    if not user_is_tagged(current_user):
        return redirect('survey')
    return render_template("results.html", MOCK_EVENTS=MOCK_EVENTS)


@app.route('/recommendations')
@login_required
def recommend():
    rec = recommender.Recommend(current_user)
    interests = rec.get_user_interests()
    events = rec.get_events()

    return render_template("recommendations.html", survey_results=interests, events=events)


def fill_user_tags(user, survey):
    db = connect_to_cloudsql()
    cursor = db.cursor()

    for items, cname in [
                            (survey.food_and_drinks, "food_drink"),
                            (survey.sports, "sports"),
                            (["adrenaline"] if survey.adrenaline else [], "adrenaline"),
                            (survey.location, "location"),
                            (survey.fitness, "fitness"),
                            (survey.arts_and_culture, "arts_culture"),
                            (survey.music, "music")
                        ]:

        for item in items:
            query = "INSERT INTO " + ENV_DB + ".UserTags(username, tag, category) VALUES ('{}', '{}', '{}')".format(current_user.username, item, cname)

            cursor.execute(query)

    db.commit()
    db.close()


def query_for_survey(user):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM " + ENV_DB + ".UserTags where username='" + user.username + "'")
    data = cursor.fetchone()
    db.close()
    return data


def user_is_tagged(user):
    result = query_for_survey(user)
    if result is None:
        return False
    else:
        return True


@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = UserInterests(request.form)

    if request.method == 'POST' and form.validate():
        survey_obj = UserInterests()
        form.populate_obj(survey_obj)

        fill_user_tags(current_user, survey_obj)

        return redirect(url_for('home'))

    return render_template('survey.html', title='Survey', form=form)


@app.route('/new_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm(request.form)

    if request.method == 'POST' and form.validate():
        event = EventForm()
        form.populate_obj(event)

        print(event.start)

        return redirect(url_for('home'))

    return render_template('event_form.html', title='New Event', form=form)




@app.errorhandler(401)
def page_not_found(e):
    error = 'You must be logged in to view this page.'
    return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
