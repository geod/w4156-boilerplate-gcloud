from datetime import date

class Event():
    def __init__(self, title, month, day, year, description):
        if title == "":
            raise ValueError("Username cannot be empty")

        self.title = title
        # self.date = date(int(year), int(month), int(day))
        self.description = description
