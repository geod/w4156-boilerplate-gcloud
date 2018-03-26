#!/usr/bin/python

import MySQLdb
import glob, os

db = MySQLdb.connect(host="gennyc-dev:us-central1:mysqldev",
                     user="root",
                     passwd="root",
                     db="Dev")

cursor = db.cursor()

os.chdir('../')
for file in glob.glob("*.csv"):
    table_name = file[:-4]
    cursor.execute("DELETE FROM " + table_name)
    with open(file, 'r') as fp:
        columns = fp.read().strip()
        for line in fp:
            cursor.execute("INSERT INTO {}({}) VALUES ({})".format(
                table_name, columns, line.strip()))
    cursor.commit()

db.close()