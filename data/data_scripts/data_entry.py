#!/usr/bin/python

import MySQLdb
import glob, os

db = MySQLdb.connect(host="35.193.223.145",
                     user="kayvon",
                     passwd="kayvon",
                     db="Dev")

print "Connected!"

cursor = db.cursor()

os.chdir('../')
for file in ('Events.csv', 'Users.csv', 'UserTags.csv', 'EventTags.csv'):
    table_name = file[:-4]

    print "Entering " + file + "..."

    cursor.execute("DELETE FROM " + table_name)
    cursor.execute("ALTER TABLE " + table_name + "AUTOINCREMENT = 1")
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

print "Finished."

db.close()