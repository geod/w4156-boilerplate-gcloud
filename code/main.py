from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask
app = Flask(__name__, static_url_path='')


# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)

@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=True)
