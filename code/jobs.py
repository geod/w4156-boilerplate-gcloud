import logging
import recommender

try:
    from google.appengine.api import mail
    from google.appengine.api import app_identity
    from google.appengine.api import taskqueue
except ImportError:
    logging.warning('google app engine unable to be imported')

from flask import Flask, render_template, redirect, url_for, request, make_response
app = Flask(__name__)
app.debug = True

# === APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'secretkey123984392032'

import os
import MySQLdb
from user_class import User
from surveys import UserInterests
from event import Event, EventForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import Resource, Api
import datetime

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

# CLOUDSQL_CONNECTION_NAME = "gennyc-dev:us-central1:mysqldev"
# CLOUDSQL_USER = "kayvon"
# CLOUDSQL_PASSWORD = "kayvon"

DB_HOST_DEV = '35.193.223.145'
# DB_HOST_DEV = "127.0.0.1" # Using for local setup

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

api = Api(app)
randomKey= '472389hewhuw873dsa4245193ej23yfehw'

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

class MailBlastCron(Resource):
    def get(self):
        task = taskqueue.add(
            method='GET',
            url='/jobs/mail/email_blast_all')
        return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta), 200
api.add_resource(MailBlastCron, '/jobs/mail/queue_emails')

class ExecuteMailBlast(Resource):
    def get(self):
        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute("SELECT username, password, email, fname, lname, dob, timezone, email_verified FROM " + ENV_DB + ".Users")
        rows = cursor.fetchall()
        for row in rows:
            user = User(*row)
            rec = recommender.Recommend(user)
            events = rec.get_events()
            event_string = ''
            for eid, ename, start_date, end_date, num_cap, num_attending, tag in events:
                event_string += "{}, {} to {}, {}/{} filled\n\n".format(ename, start_date, end_date, num_attending, num_cap)
            # print(event_string)
            body = 'Hey {},\n\nHere are some upcoming events we think you might be interested in:\n\n\n{}'.format(user.fname, event_string)
            # print(user.email)
            send_events_email(user.email, body)
        return 200
api.add_resource(ExecuteMailBlast, '/jobs/mail/blast_all')

def send_events_email(address, email_body):
    sender_address = (
        'genNYC events <curator@{}.appspotmail.com>'.format(
            app_identity.get_application_id()))
    today = datetime.datetime.now()
    subject = 'Weekly event recommendations! - {}/{}'.format(today.month, today.day)
    # print(sender_address, address, subject, email_body)
    mail.send_mail(sender_address, address, subject, email_body)

class TaskQueueTest(Resource):
    def get(self):
        task = taskqueue.add(
            method='GET',
            url='/jobs/mail/test_execute')
        return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta), 200
api.add_resource(TaskQueueTest, '/jobs/mail/test')

class ExecuteTest(Resource):
    def get(self):
        send_events_email('kss2153@columbia.edu', 'fhdjskfhjdsk test')
        return 200
api.add_resource(ExecuteTest, '/jobs/mail/test_execute')




@app.errorhandler(404)
def page_not_found(e):
    error = 'page not found'
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
