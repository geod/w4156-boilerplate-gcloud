#!/usr/bin/python

import MySQLdb
import glob, os

db = MySQLdb.connect(host="gennyc-dev:us-central1:mysqldev",
                     user="root",
                     passwd="root",
                     db="Dev")

cursor = db.cursor()

os.chdir('../')
for file in ('Events.csv', 'Locations.csv', 'Users.csv', 'UserTags.csv', 'EventTags.csv', 'Attends.csv'):
    table_name = file[:-4]
    cursor.execute("DELETE FROM " + table_name)
    with open(file, 'r') as fp:
        columns = fp.read().strip()
        for line in fp:
            processed_line = []
            for arg in line.strip().split(","):
                if arg.replace(".", "", 1).isdigit():
                    processed_line.append(arg)
                else:
                    processed_line.append("'" + arg + "'")
            cursor.execute("INSERT INTO {}({}) VALUES ({})".format(
                table_name, columns, ",".join(processed_line)))
    cursor.commit()

db.close()