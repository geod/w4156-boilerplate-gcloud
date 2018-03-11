import sys
import os
import MySQLdb

# print(sys.path)
# print(sys.modules)
sys.modules.pop('google')

from google.appengine.ext import vendor
# vendor.add('lib')
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))


from flask import Flask, render_template, redirect, url_for, request, make_response
app = Flask(__name__)

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
    return render_template("hello.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'kayvon' or request.form['password'] != 'kavyon':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

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
