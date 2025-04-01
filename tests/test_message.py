import unittest
import os
import json
from src.message_manager import MessageManager
from src.user_manager import UserManager
from src.database import Database
from create_test_data import TestData

class MassageTest(unittest.TestCase, TestData):

    def setUp(self):
        self.test_db_path = "tests/tests_data/messages"
        self.messages_file = "messages.json"
        self.users_file = "users.json"

        self.create_user_file(os.path.join(self.test_db_path, self.users_file))
        self.create_message_file(os.path.join(self.test_db_path, self.messages_file))

        self.db = Database(self.test_db_path)
        self.user_manager = UserManager(self.db)
        self.message_manager = MessageManager(self.db, self.user_manager)

    def open_file(self, path):

        with open(path, 'r') as file:
            data = json.load(file)

        return data

    def get_user_data(self, data, username):

        for user in data:
            if user['username'] == username:
                return user
            
        return None
    
    def get_user_msgs_from_inbox(self, data, username):
        
        msgs = []
        for msg in data:
            if msg['receiver'] == username:
                msgs.append({'sender': msg['sender'], 'receiver': msg['receiver'], 'message': msg['message']})
            
        return msgs
    
    def test_send_message_success(self):

        self.user_manager.logged_in_user = 'user1'

        result = self.message_manager.send_msg_to_recipient(recipient = 'user2', msg_content = 'message content')

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'The message has been sent to user2.')

        # check if data are corrected saved in database
        messages = self.open_file(os.path.join(self.test_db_path, self.messages_file))
        users = self.open_file(os.path.join(self.test_db_path, self.users_file))

        message = self.get_user_msgs_from_inbox(messages, 'user2')[0]
        user = self.get_user_data(users, 'user2')

        self.assertEqual(message['sender'], 'user1')
        self.assertEqual(message['receiver'], 'user2') 
        self.assertEqual(message['message'], 'message content')
        self.assertEqual(user["unread_msgs"], 1)

    def test_send_message_wrong_recipient(self):

        self.user_manager.logged_in_user = 'user1'

        result = self.message_manager.send_msg_to_recipient(recipient = 'wrong recipient', msg_content = 'message content')

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'There is no such user like wrong recipient.')

    def test_send_message_no_logged_user(self):

        self.user_manager.logged_in_user = None

        result = self.message_manager.send_msg_to_recipient(recipient = 'user2', msg_content = 'message content')

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'No user is currently logged in.')


    def test_send_message_too_long_message(self):

        self.user_manager.logged_in_user = 'user1'
        too_long_message = 'A' * 256

        result = self.message_manager.send_msg_to_recipient(recipient = 'user2', msg_content = too_long_message)

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Message is to long.')

    def test_send_message_full_inbox(self):

        self.user_manager.logged_in_user = 'user1'
        
        result = self.message_manager.send_msg_to_recipient(recipient = 'user3', msg_content = 'message content')

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Inbox is full.')

    def test_read_message_success(self):
        self.user_manager.logged_in_user = 'user4'
        result = self.message_manager.read_msg()

        # Check content of message
        messages = self.open_file(os.path.join(self.test_db_path, self.messages_file))
        message = self.get_user_msgs_from_inbox(messages, 'user4')[0]
        del message["receiver"]

        self.assertEqual(result[0], message)

        # Check if number of unread messaged was updated
        users = self.open_file(os.path.join(self.test_db_path, self.users_file))
        user = self.get_user_data(users, 'user4')

        self.assertEqual(user['unread_msgs'], 0)


    def test_read_message_failure_no_logged_user(self):
        
        result = self.message_manager.read_msg()

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'No user is currently logged in.')

    def test_read_message_empty_inbox(self):

        self.user_manager.logged_in_user = 'user1'
        self.user_manager.logged_in_role = 'user'

        result = self.message_manager.read_msg()  
        self.assertEqual(result["message"], "You don't have any messages.")

    def test_read_message_as_admin(self):
                
        self.user_manager.logged_in_user = 'user4'
        self.user_manager.logged_in_role = 'admin'

        result = self.message_manager.read_msg() 

        self.assertEqual(len(result), 7)

        # Check if number of unread messaged was updated
        users = self.open_file(os.path.join(self.test_db_path, self.users_file))
        user = self.get_user_data(users, 'user4')

        self.assertEqual(user['unread_msgs'], 0)        

    def tearDown(self):
        if os.path.exists(os.path.join(self.test_db_path,  self.messages_file)):
            os.remove(os.path.join(self.test_db_path,  self.messages_file))
            os.remove(os.path.join(self.test_db_path,  self.users_file))