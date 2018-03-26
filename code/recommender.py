import main


class Recommend:

    def __init__(self, user):
        self.user = user
        self.most_interested = []

    def get_user_interests(self):
        values = main.query_for_survey(self.user)
        survey_results = []
        iterresults = iter(values)
        next(iterresults)

        for x in iterresults:
            if len(x) > 1:
                survey_results.append(x)
            else:
                pass

        self.most_interested = sorted(survey_results)
        return self.most_interested


    def get_events(self):
        mock_events = {
            "wine": ["Wine Tastery", "Vino Wine"],
            "football": ["Superbowl Saturday", "Football Mania"],
            "museum": ["Pay What You Wish MoMA", "Met Gala"],
            "water": ["Water Polo Night"],
            "rock": ["Karaoke Night With Aerosmith"],
            "pilates": ["Belly Blaster"],
            "bbq": ["Dino BBQ"]
        }

        filtered = {k: mock_events[k] for k in mock_events.viewkeys() & set(self.most_interested)}
        return filtered