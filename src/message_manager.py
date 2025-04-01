from src.message import Message

class MessageManager():

    def __init__(self, database, user_manager) -> None:
        self.db = database
        self.user_manager = user_manager

    def send_msg_to_recipient(self, **kwargs):
        """Send the message and save it to the database. The message must be less than 250 characters and the recipient's inbox cannot be full.
        Args:
            recipient (str): name of recipient
            msg_content (str): content of message
        
        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        recipient = kwargs['recipient']
        msg_content = kwargs['msg_content']
        
        if not self.user_manager.is_logged_in():
            return {"status": "failure", "message": "No user is currently logged in."}
        if len(msg_content) > 255:
            return {"status": "failure", "message": "Message is to long."}
        
        users = self.db.load_data(self.db.database_path, self.db.file_users)
        user = self.db.get_user_data(users, recipient)
        if user is None:
            return {"status": "failure", "message": f"There is no such user like {recipient}."}
        
        unread_msgs = user['unread_msgs']
        if unread_msgs >= 5:
                    return {"status": "failure", "message": "Inbox is full."}        

        # save message
        message = Message(self.user_manager.get_logged_in_user(), recipient, msg_content)    
        messages = self.db.load_data(self.db.database_path, self.db.file_messages)
        messages.append(message.__dict__)
        self.db.save_data(self.db.database_path, self.db.file_messages, messages) 

        # update inbox
        unread_msgs = unread_msgs + 1
        self.db.update_unread_msgs(users, recipient, unread_msgs)
        self.db.save_data(self.db.database_path, self.db.file_users, users) 

        return {"status": "success", "message": f"The message has been sent to {recipient}."}

    
    def read_msg(self, **kwargs):
        """Read the message and update user inbox. If user is the admin, function prints messages of all users.

        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        if not self.user_manager.is_logged_in():
            return {"status": "failure", "message": "No user is currently logged in."}
        
        messages = self.db.load_data(self.db.database_path, self.db.file_messages)
        user_msgs = self.db.get_user_msgs_from_inbox( messages, self.user_manager.get_logged_in_user())
        
        if len(user_msgs) == 0 and self.user_manager.get_logged_in_role() == 'user':
            return {"message": "You don't have any messages."}
        else:
            # update user data
            users = self.db.load_data(self.db.database_path, self.db.file_users)
            self.db.update_unread_msgs(users, self.user_manager.get_logged_in_user(), 0)
            self.db.save_data(self.db.database_path, self.db.file_users, users)

            if self.user_manager.get_logged_in_role() == 'admin':
                return messages
            else:
                return user_msgs