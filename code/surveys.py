from wtforms import Form, fields, validators


class SurveyTestQuestion(Form):
    gender = fields.RadioField('What is your gender?',
                               choices=[('M', 'Male'), ('F', 'Female'), ('O', 'I prefer not to answer')],
                               validators=[validators.InputRequired()], default=('M', 'Male'))
    age = fields.RadioField('What is your age?',
                            choices=[('lt18', 'Younger than 18'), ('18-24', '18 to 24'), ('25-34', '25 to 34'),
                                     ('35-44', '35 to 44'), ('45-54', '45 to 54'), ('55', '55 years or older')],
                            validators=[validators.InputRequired()])
    education = fields.RadioField('Which of the following best describes your highest education level?',
                                  choices=[('Hsg', 'High school graduate'),
                                           ('Scnd', 'Some college, no degree'), ('Assoc', 'Associates Degree'),
                                           ('Bach', 'Bachelors degree'),
                                           ('Grad', 'Graduate degree (Masters, Doctorate, etc.)'),
                                           ('O', 'Other')],
                                  validators=[validators.InputRequired()])
    language = fields.StringField('What is your native language', validators=[validators.InputRequired()])


class UserInterests(Form):
    food_and_drinks = fields.SelectMultipleField('Choose your favorite food and drink options',
                                                 choices=[('desserts', 'Desserts'), ('wine', 'Wine tasting'),
                                                          ('beer', 'Beer'), ('vegetarian', 'Vegetarian'),
                                                          ('vegan', 'Vegan'), ('meats', 'Meats'),
                                                          ('bbq', 'BBQ'), ('tapas', 'Tapas'),
                                                          ('brunch', 'Basic Brunch'),('romantic', 'Romantic'),
                                                          ('trendy', 'Trendy'), ('diy', 'DIY'), ('none_food', 'None')],
                                                 validators=[validators.InputRequired()])
    sports = fields.SelectMultipleField('What sports do you like?',
                                        choices=[('soccer', 'Soccer'), ('football', 'Football'),
                                                 ('basketball', 'Basketball'), ('baseball', 'Baseball'),
                                                 ('tennis', 'Tennis'), ('lax', 'Lacross'),
                                                 ('hockey', 'Hockey'), ('golf', 'Golf'),
                                                 ('other_sport', 'Other'), ('none_sport', 'Not interested')],
                                        validators=[validators.InputRequired()])
    adrenaline = fields.BooleanField('Do you like adrenaline adventures?')
    location = fields.SelectMultipleField('What suits you?',
                                          choices=[('indoors', 'Indoors'), ('outdoors', 'Outdoors'),
                                                   ('water', 'On the Water'), ('any', 'Anywhere!')],
                                          validators=[validators.InputRequired()])
    fitness = fields.SelectMultipleField('What do you like to do for exercise?',
                                         choices=[('dance', 'Dance'), ('pilates', 'Pilates'),
                                                   ('boxing', 'Boxing'), ('yoga', 'Yoga'),
                                                   ('spin', 'Spin'), ('sculpting', 'Body Sculpting'),
                                                   ('other_fitness', 'Other'), ('none_fitness', 'Not interested')],
                                         validators=[validators.InputRequired()])
    arts_and_culture = fields.SelectMultipleField('What kinds of arts & culture interest you?',
                                         choices=[('painting', 'Painting'), ('museum', 'Museum/Gallery'),
                                                  ('theater', 'Theater'), ('lecture', 'Lecture'),
                                                  ('other_art', 'Other'), ('none_arts', 'Not interested')],
                                         validators=[validators.InputRequired()])
    music = fields.SelectMultipleField('Do you any of these music options sing to you?',
                                       choices=[('clubbing', 'Clubbing'), ('rock', 'Rock'),
                                                ('pop', 'Pop'), ('classical', 'Classical'),
                                                ('karaoke', 'Karaoke'), ('other_music', 'Other'),
                                                ('none_music', 'Not interested')],
                                       validators=[validators.InputRequired()])
