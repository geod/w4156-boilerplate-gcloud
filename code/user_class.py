class User():
    def __init__(self, username, password):
        if username == "":
            raise ValueError("Username cannot be empty")
        if password == "":
            raise ValueError("Password cannot be empty")

        self.username = username
        self.password = password

    def __eq__(self, other):
        if self.username == other.username and self.password == other.password:
            return True
        else:
            return False
