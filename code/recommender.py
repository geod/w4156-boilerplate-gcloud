import main

ENV_DB = 'Dev'


class Recommend:

    def __init__(self, user):
        self.user = user
        self.most_interested = []

    def get_user_interests(self):
        db = main.connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute("SELECT tag FROM " + ENV_DB + ".UserTags WHERE username='" + self.user.username + "'")
        data = cursor.fetchall()
        db.close()

        self.most_interested = sorted([i[0] for i in data])
        return self.most_interested

        # values = main.query_for_survey(self.user)
        # survey_results = []
        # iterresults = iter(values)
        # next(iterresults)

        # for x in iterresults:
        #     if len(x) > 1:
        #         survey_results.append(x)
        #     else:
        #         pass

        # self.most_interested = sorted(survey_results)
        # return self.most_interested


    def get_events(self):
        db = main.connect_to_cloudsql()
        cursor = db.cursor()

        query = """
                SELECT DISTINCT E.eid, E1.ename, E1.start_date, E1.end_date, E1.num_cap, E1.num_attending, E.tag
                FROM {}.EventTags AS E, {}.UserTags AS U, {}.Events as E1
                WHERE U.username='{}' AND
                    E.tag = U.tag AND
                    E1.eid = E.eid
                """.format(
                        ENV_DB,
                        ENV_DB,
                        ENV_DB,
                        self.user.username
                    )

        cursor.execute(query)
        data = cursor.fetchall()
        db.close()

        return sorted([i for i in data])

        # mock_events = {
        #     "wine": ["Wine Tastery", "Vino Wine"],
        #     "football": ["Superbowl Saturday", "Football Mania"],
        #     "museum": ["Pay What You Wish MoMA", "Met Gala"],
        #     "water": ["Water Polo Night"],
        #     "rock": ["Karaoke Night With Aerosmith"],
        #     "pilates": ["Belly Blaster"],
        #     "bbq": ["Dino BBQ"]
        # }

        # filtered = {k: mock_events[k] for k in mock_events.viewkeys() & set(self.most_interested)}
        # return filtered