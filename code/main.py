from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask, make_response
app = Flask(__name__)

import os
import MySQLdb

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


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
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

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
        res+= ('{}\n'.format(r[0]))

    response = make_response(res)
    response.headers['Content-Type'] = 'text/json'

    return response

if __name__ == '__main__':
    app.run(debug=True)


