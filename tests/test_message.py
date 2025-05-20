import unittest
from src.message_manager import MessageManager
from src.user_manager import UserManager
from src.database import Database
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return config

class MessageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.db = Database(cls.config)
        cls.conn = cls.db.conn
        cls.cur = cls.conn.cursor()
        cls.cur.execute(
            """
            DROP TABLE IF EXISTS messages;
            CREATE TABLE messages (
                msg_id SERIAL PRIMARY KEY,
                sender_name VARCHAR(255) NOT NULL,
                receiver_name VARCHAR(255) NOT NULL,
                message VARCHAR(255)
            );

            DROP TABLE IF EXISTS users;
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(5) NOT NULL,
                unread_msgs INTEGER NOT NULL
            );
            """
        )
        cls.conn.commit()

    def setUp(self):
        self.user_manager = UserManager(self.db)
        self.message_manager = MessageManager(self.db, self.user_manager)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            DELETE FROM users;
            DELETE FROM messages;

            INSERT INTO messages (sender_name, receiver_name, message)
            VALUES
            ('user1', 'user3', 'msg1'),
            ('user1', 'user3', 'msg2'),
            ('user1', 'user3', 'msg3'),
            ('user1', 'user3', 'msg4'),
            ('user1', 'user3', 'msg5'),
            ('user1', 'user4', 'msg1'),
            ('user2', 'user4', 'msg2'); 

            INSERT INTO users (username, password, role, unread_msgs)
            VALUES 
            ('user1', '1234', 'user', 0),
            ('user2', '1234', 'admin', 0),
            ('user3', '1234', 'user', 5),
            ('user4', '1234', 'user', 2);
            """
        )
        self.conn.commit()

    def get_user_data(self, username):
        self.cur.execute("SELECT username, password, role, unread_msgs FROM users WHERE username = %s", (username,))
        row = self.cur.fetchone()
        if row:
            return {
                "username": row[0],
                "password": row[1],
                "role": row[2],
                "unread_msgs": row[3]
            }
        return None

    def get_user_msgs_from_inbox(self, username):
        self.cur.execute("SELECT sender_name, receiver_name, message FROM messages WHERE receiver_name = %s", (username,))
        msgs = []
        for row in self.cur.fetchall():
            msgs.append({'sender': row[0], 'receiver': row[1], 'message': row[2]})
        return msgs

    def test_send_message_success(self):
        self.user_manager.logged_in_user = 'user1'
        result = self.message_manager.send_msg_to_recipient(recipient='user2', msg_content='message content')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'The message has been sent to user2.')

        # check if data are correctly saved in database
        messages = self.get_user_msgs_from_inbox('user2')
        users = self.get_user_data('user2')

        message = messages[0]
        user = users

        self.assertEqual(message['sender'], 'user1')
        self.assertEqual(message['receiver'], 'user2')
        self.assertEqual(message['message'], 'message content')
        self.assertEqual(user["unread_msgs"], 1)

    def test_send_message_wrong_recipient(self):
        self.user_manager.logged_in_user = 'user1'
        result = self.message_manager.send_msg_to_recipient(recipient='wrong recipient', msg_content='message content')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'There is no such user like wrong recipient.')

    def test_send_message_no_logged_user(self):
        self.user_manager.logged_in_user = None
        result = self.message_manager.send_msg_to_recipient(recipient='user2', msg_content='message content')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'No user is currently logged in.')

    def test_send_message_too_long_message(self):
        self.user_manager.logged_in_user = 'user1'
        too_long_message = 'A' * 256
        result = self.message_manager.send_msg_to_recipient(recipient='user2', msg_content=too_long_message)
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Message is to long.')

    def test_send_message_full_inbox(self):
        self.user_manager.logged_in_user = 'user1'
        result = self.message_manager.send_msg_to_recipient(recipient='user3', msg_content='message content')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Inbox is full.')

    def test_read_message_success(self):
        self.user_manager.logged_in_user = 'user4'
        result = self.message_manager.read_msg()

        # Check content of message
        messages = self.get_user_msgs_from_inbox('user4')
        message = messages[0]
        # Dopasuj klucze do formatu zwracanego przez read_msg
        expected = {
            "sender_name": message["sender"],
            "message": message["message"]
        }

        self.assertEqual(dict(result[0]), expected)

        # Check if number of unread messages was updated
        user = self.get_user_data('user4')
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
        print(result)
        self.assertEqual(len(result), 7)
        # Check if number of unread messages was updated
        user = self.get_user_data('user4')
        self.assertEqual(user['unread_msgs'], 0)

    @classmethod
    def tearDownClass(cls):
        cls.cur.execute("DROP TABLE IF EXISTS messages;")
        cls.cur.execute("DROP TABLE IF EXISTS users;")
        cls.conn.commit()
        cls.cur.close()
        cls.conn.close()