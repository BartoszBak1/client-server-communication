import json
import os

class Database():
    def __init__(self, database_path = "/Projects/zero_to_junior/backend/python_201/data") -> None:
        self.database_path = database_path 
        self.file_users = "users.json"
        self.file_messages = "messages.json"

    def save_data(self, path, file_name, data):
        """Save data in json.

        Args:
            path (str): path to file
            file_name (str): name of the file
            data (json): data
        """
        with open(os.path.join(path, file_name), "w") as file:
            json.dump(data, file)

    def load_data(self, path, file_name):
        """Load data from json file.

        Args:
            path (str): path to file
            file_name (str): name of the file

        Returns:
            json: data from file
        """
        with open(os.path.join(path, file_name), "r") as file:
            return json.load(file)
        
    def check_if_user_exist(self, users, username):
        """Check if user exists in database.

        Args:
            users (dict): Dictionary with users.
            username (str): Name of the user you are looking for.

        Returns:
            bool: True or False
        """
        for user in users:
            if username == user["username"]:
                return True
        return False

    def check_credentials(self, user, username, password):
        """Check if username and password are correct.

        Args:
            user (str): user data
            username (str): username from user
            password (str): password from user

        Returns:
            bool: True or False
        """
        try:
            if username == user["username"] and password == user["password"]:
                return True
            else:
                return False
        except TypeError:
            return False   

    def get_user_data(self, data, username):
        """Get selected user's data from users's data.

        Args:
            data (dict): all users's data
            username (str): name of user

        Returns:
            dict: data of selected user
        """
        for user in data:
            if user['username'] == username:
                return user
            
        return None
    
    def get_user_msgs_from_inbox(self, data, username):
        """Get messages of user from inbox.

        Args:
            data (dict): dictionary with all messages
            username (str): name of user

        Returns:
            list: messages of user
        """
        msgs = []
        for msg in data:
            if msg['receiver'] == username:
                msgs.append({'sender': msg['sender'], 'message': msg['message']})
            
        return msgs

    def update_unread_msgs(self, users, username, new_count):

        """Update number of unread messages.

        Returns:
            bool: True or False
        """
        for user in users:
            if user['username'] == username:
               user['unread_msgs'] = new_count
               return True
        return False
