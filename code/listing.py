from datetime import date, datetime, timedelta

class Listing:
    expiryTime = timedelta(year=2018)

    def __init__(self, expiryTime, uni, place):
        self.expiryTime = expiryTime
        self.uni = uni
        self.place = place
