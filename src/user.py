class User:

    def __init__(self, username, password, role) -> None:
        self.username = username
        self.password = password
        self.role = role
        self.unread_msgs = 0