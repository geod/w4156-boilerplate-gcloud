# import meetup.api
import sys
import requests
import json
import subprocess
import MySQLdb
import datetime
import string
import re

MEETUP_API_KEY  = '6e735a762056651032171a3d106b4d78'
MEETUP_API_BASE = 'https://api.meetup.com'

URL_RE  = r'^https?:\/\/.*[\r\n]*'
TAG_RE = r'</?([a-z][a-z0-9]*)\b[^>]*>'

CATEGORY_LIMIT = 20
MIN_CHARS_DESC = 200

headers = {'Content-Type': 'application/json'}
params = {'key' : MEETUP_API_KEY}

interactive = False
verbose = True

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print "usage: python2 get_event.py [-v] [-i] <valid-event-url> "
        sys.exit(1)

    for opt in (sys.argv[1:-1]):
        if opt == "-i":
            interactive = True
        elif opt == "-v":
            verbose = True

    EVENT_URL = sys.argv[-1]

    tmp = EVENT_URL[23:-1].split("/")
    tmp.remove('events')

    URLNAME, EVENT_ID = tmp

    api_url = '{0}/{1}/events/{2}'.format(MEETUP_API_BASE, URLNAME, EVENT_ID)

    r = requests.get(api_url, headers=headers, params=params)

    if r.status_code == 200:
        # event information
        pass
    else:
        if verbose:
            print "Get event failed"
        sys.exit(1)

    event_info = json.loads(r.content.decode('utf-8'))

    if len(event_info['description']) < MIN_CHARS_DESC:
        if verbose:
            print "Failure: event description too short (>={} chars needed)".format(MIN_CHARS_DESC)
        sys.exit(1)

    wp = open('../textrank/textrank_input.txt', 'w')

    revised = event_info["description"].encode('ascii', 'ignore')
    revised = re.sub(URL_RE, ' ', revised)    
    revised = re.sub(TAG_RE, ' ', revised)
    revised = revised.translate(None, string.punctuation).replace('\r\n', ' ').replace('"', ' ').replace("'", ' ')
    
    wp.write(revised.encode('utf-8'))
    wp.close()

    process = subprocess.Popen("./run_model.sh", cwd="../textrank/")
    process.wait()

    rp = open('../textrank/textrank_output.txt', 'r')

    counter = 0
    my_words = []

    if interactive:
        print "Press 'enter' to approve, enter any key to reject"

    for line in rp:
        if line.count(":") > 1:
            continue
        if interactive:
            choice = raw_input("Accept tag " + line.split(":")[0] + "? ")
        if interactive and choice != '':
            continue
        else:
            my_words.append(tuple(line.strip().split(":")))
            counter += 1
        if counter >= CATEGORY_LIMIT:
            break

    if counter == CATEGORY_LIMIT and verbose:
        print "All {0} categories found".format(CATEGORY_LIMIT)
    elif verbose:
        print "Using {0} categories".format(counter)

    rp.close()

    if verbose:
        print [i[0] for i in my_words]

    if interactive:
        if raw_input("Press ENTER to approve and send to db, or other key to exit: ") != "":
            print "Exited"
            sys.exit(1)

    # print event_info


    db = MySQLdb.connect(host="127.0.0.1",
                     user="root",
                     passwd="root",
                     db="Dev")


    # event_info['lon']
    # event_info['lat']
    # event_info['name']
    # event_info['venue']['address_1']
    # event_info['venue']['zip']
    # event_info['venue']['city']
    # event_info['venue']['state']


    if verbose:
        print "Connected to database"

    cursor = db.cursor()

    loc_query = """
                INSERT 
                INTO Locations(lname, lat, lon, address_1, zip, city, state) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

    cursor.execute(loc_query, ( event_info['venue']['name'],
                                event_info['venue']['lon'],
                                event_info['venue']['lat'],
                                event_info['venue']['address_1'],
                                event_info['venue']['zip'],
                                event_info['venue']['city'],
                                event_info['venue']['state']))

    db.commit()

    print "Inserted into Locations."

    cursor.execute("SELECT LAST_INSERT_ID()")

    lid = cursor.fetchone()

    start_date = str(datetime.datetime.fromtimestamp(event_info['time'] / 1000))
    end_date = str(datetime.datetime.fromtimestamp((event_info['time'] + event_info['duration']) / 1000))

    ev_query =  """
                INSERT
                INTO Events(ename, start_date, end_date, 
                            num_attending, lid, description)
                VALUES (%s, %s, %s, %s, %s, %s);
                """

    cursor.execute(ev_query,   (event_info['name'].encode('ascii', 'ignore'),
                                start_date,
                                end_date,
                                0,
                                lid,
                                event_info['description'].encode('ascii', 'ignore')))

    db.commit()

    print "Inserted into Events."

    cursor.execute("SELECT LAST_INSERT_ID()")

    eid = cursor.fetchone()

    for tag, relevance in my_words:
        et_query =  """
                    INSERT
                    INTO EventTags(eid, tag, relevance)
                    VALUES (%s, %s, %s)
                    """

        cursor.execute(et_query,( eid,
                                  tag,
                                  relevance))

    db.commit()

    print "Inserted into EventTags."

    if verbose:
        print "Finished."

    db.close()


#################
    # api_url = '{0}/{1}'.format(MEETUP_API_BASE, URLNAME)

    # r = requests.get(api_url, headers=headers, params=params)

    # if r.status_code == 200:
    #     # event information
    #     pass
    # else:
    #     print "Get group failed"
    #     sys.exit(1)

    # group_info = json.loads(r.content.decode('utf-8'))
    # print group_info
################
    # client = meetup.api.Client(MEETUP_API_KEY)

    # # group_info = client.GetGroup({'urlname': SITE_URL})
    # # print group_info.name

    # event_info = client.GetEvent(id=SITE_URL)

    # print event_info.group

    # print client.GetGroup({'urlname': event_info.group[unicode('urlname')]}).__dict__.keys()

    # # print client.GetMembers(group_id=SITE_URL).__dict__.keys()
