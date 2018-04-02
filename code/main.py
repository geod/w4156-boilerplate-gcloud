from __future__ import print_function
from google.appengine.ext import vendor
import os
from user import *

vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
from flask import Flask, make_response, request, url_for, redirect
import MySQLdb

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ['CLOUDSQL_CONNECTION_NAME']
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

app = Flask(__name__, static_url_path='')

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

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        # just connect directly to cloud SQL lul
        db = MySQLdb.connect(
            host='35.227.27.169', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db


@app.route('/')
def index():
    return "Hello, World (lets see how long a change takes III)!"


@app.route('/databases')
def showDatabases():
    """Simple request handler that shows all of the MySQL SCHEMAS/DATABASES."""

    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('SHOW SCHEMAS')

    res = ""
    for r in cursor.fetchall():
        res += ('{}\n'.format(r[0]))

    response = make_response(res)
    response.headers['Content-Type'] = 'text/json'

    # disconnect from db after use
    db.close()

    return response


@app.route('/index.html', methods=['POST'])
def create_user():
    firstname = request.form['first_name_field']
    lastname = request.form['last_name_field']
    uni = request.form['uni_field']
    password = request.form['password_field']
    school = request.form['school_field']
    year = request.form['year_field']
    interests = request.form['interests_field']

    name = firstname + ' ' + lastname
    user = User(uni, name, year, interests, school, password)

    # need to take in whether user needs swipes

    print(user.uni + user.name + user.schoolYear + user.interests + user.schoolName + user.password)

    # store in database

    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('use cuLunch')

    query = "INSERT INTO users VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (uni, password, name, year, interests, school)
    # print('query generated')
    # print(query)

    try:
        cursor.execute(query)
        # commit the changes in the DB
        db.commit()
    except:
        # rollback when an error occurs
        db.rollback()

    # disconnect from db after use
    db.close()

    return redirect(url_for('static', filename='listform/index.html'))


@app.route('/listform/index.html', methods=['POST'])
def create_listing():
    cafeteria = request.form['Cafeteria']

    print(cafeteria)

    # store in database
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('use cuLunch')

    query = "INSERT INTO listings VALUES ('%s', '%s', '%d', '%s')" % ('2018-04-20 19:00:05', 'cl3403', True, cafeteria)
    #print('query generated')
    #print(query)

    try:
        cursor.execute(query)
        # commit the changes in the DB
        db.commit()
    except:
        # rollback when an error occurs
        db.rollback()

    # disconnect from db after use
    db.close()

    return redirect(url_for('static', filename='listings/index.html'))

if __name__ == '__main__':
    app.run(debug=True)
