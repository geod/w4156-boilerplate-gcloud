## How to enter data
Currently, the system pulls events from Meetup's API to server as mock data. To add an event:
1. Navigate to the event of your choice (`https://www.meetup.com/group_name/events/event_id/`)
2. `cd data_retrieval`
3. Make sure your database is running locally! (See below)
4. `python event_pipeline.py [-v] [-i] <valid-event-url>`
  - `-v` is verbose (it is on by default)
  - `-i` is interactive, which lets you hand-pick the tags
5. The script will then infer tags based on the event's description, and enter those into the database, along with the event's information and its location.

## How to run database locally
Google Cloud SQL does not allow you to directly connect using Python's `MySQLdb` package. Instead, you need to run a proxy. In order to do that, follow [this link](https://cloud.google.com/python/getting-started/using-cloud-sql) or read below.

1. `cd data`
2. Download proxy: `wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy`
3. `chmod +x cloud_sql_proxy`
4. `gcloud auth application-default login`. A browser window should have opened. Log into your Google Cloud account.
5. `kill mysqld` (to free port 3306)
6. `./cloud_sql_proxy -instances="gennyc-dev:us-central1:mysqldev"=tcp:3306`

Your proxy server will be running at `127.0.0.1:3306`. Route all MySQLdb requests to there, and it should work:
```python
db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="root",
                     db="Dev")

cursor = db.cursor()

# code here...

db.close()
```
