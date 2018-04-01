# import meetup.api
import sys
import requests
import json

MEETUP_API_KEY  = '6e735a762056651032171a3d106b4d78'
MEETUP_API_BASE = 'https://api.meetup.com'

headers = {'Content-Type': 'application/json'}

params = {'key' : MEETUP_API_KEY}

def main():
    if len(sys.argv) != 2:
        print ("usage: python2 get_event.py <valid-event-url>")
        sys.exit(1)

    EVENT_URL = sys.argv[1]

    tmp = EVENT_URL[23:-1].split("/")
    tmp.remove('events')

    URLNAME, EVENT_ID = tmp

    api_url = '{0}/{1}/events/{2}'.format(MEETUP_API_BASE, URLNAME, EVENT_ID)

    r = requests.get(api_url, headers=headers, params=params)

    if r.status_code == 200:
        # event information
        pass
    else:
        print("Get event failed")
        sys.exit(1)

    event_info = json.loads(r.content.decode('utf-8'))
    print(event_info)

    api_url = '{0}/{1}'.format(MEETUP_API_BASE, URLNAME)

    r = requests.get(api_url, headers=headers, params=params)

    if r.status_code == 200:
        # event information
        pass
    else:
        print("Get group failed")
        sys.exit(1)

    group_info = json.loads(r.content.decode('utf-8'))
    print(group_info)

    # client = meetup.api.Client(MEETUP_API_KEY)

    # # group_info = client.GetGroup({'urlname': SITE_URL})
    # # print group_info.name

    # event_info = client.GetEvent(id=SITE_URL)

    # print event_info.group

    # print client.GetGroup({'urlname': event_info.group[unicode('urlname')]}).__dict__.keys()

    # # print client.GetMembers(group_id=SITE_URL).__dict__.keys()




if __name__ == "__main__":
    main()