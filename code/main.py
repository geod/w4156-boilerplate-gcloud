from __future__ import print_function
from google.appengine.ext import vendor
import os
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
import os
import MySQLdb
import sqlite3
import sys

from flask import Flask, make_response
app = Flask(__name__, static_url_path='')


# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ['CLOUDSQL_CONNECTION_NAME']
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

LOCAL_DATABASE = 'cuLunch_main.db'
SCHEMA_PATH = "../schemas/cuLunch_schema.sql"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(LOCAL_DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA_PATH, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # this only runs in prod

        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        print("GOT here", file=sys.stderr)

        print("trying to connect to {}".format(CLOUDSQL_CONNECTION_NAME), file=sys.stderr)


        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    else:
        # devving locally
        """
        print(os.getenv('SERVER_SOFTWARE', ''), file=sys.stderr)
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)
        """
        init_db()
        db = get_db()

    return db

@app.route('/')
def index():
    return "Hello, World (lets see how long a change takes III)!"

@app.route('/databases')
def showDatabases():
    """Simple request handler that shows all of the MySQL SCHEMAS/DATABASES."""
    print("DBBBBBBBBBBBBBBBBB", file=sys.stderr)

    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('SHOW SCHEMAS')

    res = ""
    for r in cursor.fetchall():
        res+= ('{}\n'.format(r[0]))

    response = make_response(res)
    response.headers['Content-Type'] = 'text/json'

    return response

if __name__ == '__main__':
    app.run(debug=True)


