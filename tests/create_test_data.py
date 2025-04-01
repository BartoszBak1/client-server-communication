import json

class TestData():

    def __init__(self) -> None:
        return

    def create_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f)

    def create_user_file(self, path):

        data = [
            {
                "username": "user1",
                "password": "1234",
                "role": "user",
                "unread_msgs": 0
            },
            {
                "username": "user2",
                "password": "1234",
                "role": "admin",
                "unread_msgs": 0
            },
            {
                "username": "user3",
                "password": "1234",
                "role": "user",
                "unread_msgs": 5
            },
            {
                "username": "user4",
                "password": "1234",
                "role": "user",
                "unread_msgs": 2
            }
        ]
        self.create_file(path, data)
        
    def create_message_file(self, path):
        data = [

        {
            "sender": "user1",
            "receiver": "user3",
            "message": "msg1"
        },
        {
            "sender": "user1",
            "receiver": "user3",
            "message": "msg2"
        },
        {
            "sender": "user1",
            "receiver": "user3",
            "message": "msg3"
        },
        {
            "sender": "user1",
            "receiver": "user3",
            "message": "msg4"
        },
        {
            "sender": "user1",
            "receiver": "user3",
            "message": "msg5"
        },

        {
            "sender": "user1",
            "receiver": "user4",
            "message": "msg1"
        },
        {
            "sender": "user2",
            "receiver": "user4",
            "message": "msg2"
        },
    ]
        self.create_file(path, data)        