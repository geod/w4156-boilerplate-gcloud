from wtforms import Form, fields, validators
from datetime import datetime, date
from wtforms_components import TimeField
from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms.ext.dateutil.fields import DateTimeField

class Event():
    def __init__(self, title, month, day, year, description):
        if title == "":
            raise ValueError("Username cannot be empty")

        self.title = title
        # self.date = date(int(year), int(month), int(day))
        self.description = description

class EventForm(Form):
    currentDate = date.today()
    today = currentDate.strftime('%m/%d/%Y')

    event_name = fields.StringField("Name your event:", validators=[validators.InputRequired()])
    description = fields.TextAreaField("Event description:", validators=[validators.InputRequired()])
    formatted_address = fields.StringField("Location Address:", validators=[validators.InputRequired()])
    start_date = DateTimeField('When will it start?', display_format='%Y-%m-%d %H:%M', validators=[validators.InputRequired()],
        render_kw={"type": "datetime-local"})
    end_date = DateTimeField('When will it end?', display_format='%Y-%m-%d %H:%M', validators=[validators.InputRequired()],
        render_kw={"type": "datetime-local"})
    cap = fields.IntegerField("Maximum number of people able to participate:", validators=[])
    attending = fields.IntegerField("How many people are attending already?", validators=[])

    # location parsing fields (hidden)
    lat = fields.StringField("Latitude:")
    lng = fields.StringField("Longitude:")
    name = fields.StringField("Location Name:")
    address_2 = fields.StringField("Address Line 2:")
    postal_code = fields.StringField("Zip code:")
    sublocality = fields.StringField("City:")
    administrative_area_level_1_short = fields.StringField("State:")
