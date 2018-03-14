import main

class User():
    def __init__(self, username, password):
        if username == "":
            raise ValueError("Username cannot be empty")
        if password == "":
            raise ValueError("Password cannot be empty")

        self.username = username
        self.password = password
        self.authenticated = True

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
