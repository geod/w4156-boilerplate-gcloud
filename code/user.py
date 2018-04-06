from listing import Listing

class User:

    def __init__(self, uni, name, year, interests, school, password):
        self.uni = uni
        self.name = name
        self.schoolYear = year
        self.interests = interests
        self.school = school
        self.password = password
        self.listings = []

    def add_listing(self, listing):
        self.listings.append(self, listing)

    def create_listing(self, expiry_time, place):
        listing = Listing(expiry_time, self.uni, place)
        self.add_listing(listing)


class Form:

    def __init__(self, f_name, l_name, uni, pwd, school, year, interests):
        # type: (object, object, object, object, object, object, object) -> object
        self.uni = uni
        self.f_name = f_name
        self.l_name = l_name
        self.year = year
        self.interests = interests
        self.school = school
        self.pwd = pwd

    def form_input_valid(self):
        uChecker = True
        if self.f_name == "" or self.l_name == "" or self.uni == "" or self.pwd == "":
            uChecker = False
        elif len(self.pwd) < 8 or self.pwd.isupper() or self.pwd.islower() or self.pwd.isdigit():
            uChecker = False
        return uChecker