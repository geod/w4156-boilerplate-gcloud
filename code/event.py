from datetime import date
from wtforms import Form, fields, validators


class Event():
    def __init__(self, title, month, day, year, description):
        if title == "":
            raise ValueError("Username cannot be empty")

        self.title = title
        # self.date = date(int(year), int(month), int(day))
        self.description = description


class EventForm(Form):
    name = fields.StringField("Name your event:", validators=[validators.InputRequired()])
    start = fields.DateField("When will it start?", format="%Y-%m-%dT%H:%M", validators=[validators.InputRequired()])
    end = fields.DateField("When will it start?", format="%Y-%m-%dT%H:%M", validators=[validators.InputRequired()])
    cap = fields.IntegerField("Maximum number of people able to participate:", validators=[])
    attending = fields.IntegerField("How many people are attending already?", validators=[])
