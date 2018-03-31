from listing import Listing

class User:

    def __init__(self, uni, name, schoolYear, interests, needsSwipes, schoolName, password):
        self.uni = uni
        self.name = name
        self.schoolYear = schoolYear
        self.interests = interests
        self.needsSwipes = needsSwipes
        self.schoolName = schoolName
        self.password = password
        self.listings = []

    def add_listing(self, listing):
        self.listings.append(self, listing)

    def create_listing(self, expiryTime, place):
        listing = Listing(expiryTime, self.uni, place)
        self.add_listing(listing)
