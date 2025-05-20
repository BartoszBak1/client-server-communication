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
        
        if self.db.check_data({"query": "query_check_if_user_exist", "query_arguments": {"username": recipient}}) == False:
            return {"status": "failure", "message": f"There is no such user like {recipient}."}
        
        user = self.db.get_data({"query": "query_get_user_data", "query_arguments": {"username": recipient}})[0]
        unread_msgs = user['unread_msgs']
        if unread_msgs >= 5:
                    return {"status": "failure", "message": "Inbox is full."}        

        # save message
        message = Message(self.user_manager.get_logged_in_user(), recipient, msg_content)
        self.db.save_data({"query": "query_insert_message", "query_arguments": message.__dict__})

        # update inbox
        unread_msgs = unread_msgs + 1
        self.db.save_data({"query": "query_update_unread_msgs", "query_arguments": {'unread_msgs': unread_msgs, 'username': recipient}})

        return {"status": "success", "message": f"The message has been sent to {recipient}."}

    
    def read_msg(self, **kwargs):
        """Read the message and update user inbox. If user is the admin, function prints messages of all users.

        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        if not self.user_manager.is_logged_in():
            return {"status": "failure", "message": "No user is currently logged in."}
        
        user_msgs = self.db.get_data({"query": "query_get_user_messages", "query_arguments": {'receiver': self.user_manager.get_logged_in_user()}})
        print(user_msgs)
        if len(user_msgs) == 0 and self.user_manager.get_logged_in_role() == 'user':
            return {"message": "You don't have any messages."}
        else:
            self.db.save_data({"query": "query_update_unread_msgs", "query_arguments": {'unread_msgs': 0, 'username': self.user_manager.get_logged_in_user()}})

            if self.user_manager.get_logged_in_role() == 'admin':
                messages = self.db.get_data({"query": "query_get_all_messages", "query_arguments": {}})
                return messages
            else:
                return user_msgs