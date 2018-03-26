import main

ENV_DB = 'Dev'


class Recommend:

    def __init__(self, user, db_conn_func):
        self.db_conn_func = db_conn_func
        self.user = user
        self.most_interested = []

    def get_user_interests(self):
        db = db_conn_func()
        cursor = db.cursor()
        cursor.execute("SELECT tag FROM " + ENV_DB + ".UserTags WHERE username='" + self.user.user_name + "'")
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
        db = db_conn_func()
        cursor = db.cursor()

        query = """
                SELECT DISTINCT E.eid 
                FROM {}.EventTags AS E, {}.UserTags AS U 
                WHERE U.username='{}' AND
                    E.tag = U.tag
                """.format(
                        ENV_DB,
                        ENV_DB,
                        self.user.user_name
                    )

        cursor.execute(query)
        data = cursor.fetchall()
        db.close()

        return sorted([i[0] for i in data])

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