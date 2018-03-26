import main
import datetime

class User():
    def __init__(self, username, password, email=None, fname=None, lname=None, dob=None, timezone=None):
        if username == "":
            raise ValueError("Username cannot be empty")
        if password == "":
            raise ValueError("Password cannot be empty")

        self.username = username
        self.password = password
        self.authenticated = True
        self.email = email
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.timezone = timezone
        self.join_date = datetime.date.today()

        # print self.email, self.dob, self.timezone, self.join_date
        # print type(self.email), type(self.dob), type(self.timezone), type(self.join_date)

    def __eq__(self, other):
        if self.username == other.username and self.password == other.password:
            return True
        else:
            return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
