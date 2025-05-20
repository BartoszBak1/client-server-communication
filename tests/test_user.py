import unittest
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

class UserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.db = Database(cls.config)
        cls.conn = cls.db.conn
        cls.cur = cls.conn.cursor()
        cls.cur.execute(
            """
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
        self.cur.execute("DELETE FROM users;")
        self.cur.execute(
            """
            INSERT INTO users (username, password, role, unread_msgs)
            VALUES 
            ('user1', '1234', 'user', 0),
            ('user2', '1234', 'admin', 0),
            ('user3', '1234', 'user', 5),
            ('user4', '1234', 'user', 2);
            """
        )
        self.conn.commit()
        self.user_credentials = {
            "username": "test_user",
            "password": "123456",
            "role": "user",
        }

    def test_create_account_success(self):
        result = self.user_manager.create_account(**self.user_credentials)
        self.assertEqual(result["status"], "success")
        self.assertEqual(
            result["message"], "You have created new account named test_user."
        )

    def test_create_account_failure(self):
        self.user_manager.create_account(**self.user_credentials)
        result = self.user_manager.create_account(**self.user_credentials)
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "User with that name already exist.")

    def test_create_account_wrong_role(self):
        result = self.user_manager.create_account(
            username="test_user", password="123456", role="xxxx"
        )
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "Wrong role. Select user or admin.")

    def test_login_success(self):
        self.user_manager.create_account(**self.user_credentials)
        result = self.user_manager.login(username="test_user", password="123456")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "User test_user logged in.")
        self.assertEqual(self.user_manager.logged_in_user, "test_user")
        self.assertEqual(self.user_manager.logged_in_role, "user")

    def test_login_wrong_name(self):
        self.user_manager.create_account(**self.user_credentials)
        result = self.user_manager.login(username="wrong_name", password="123456")
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "Invalid username or password.")
        self.assertEqual(self.user_manager.logged_in_user, None)

    def test_login_wrong_password(self):
        self.user_manager.create_account(**self.user_credentials)
        result = self.user_manager.login(
            username="test_user", password="wrong_password"
        )
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "Invalid username or password.")
        self.assertEqual(self.user_manager.logged_in_user, None)

    def test_login_already_login(self):
        self.user_manager.create_account(**self.user_credentials)
        self.user_manager.login(username="test_user", password="123456")
        result = self.user_manager.login(username="test_user", password="123456")
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "You are logged in as test_user.")

    def test_logout_success(self):
        self.user_manager.create_account(**self.user_credentials)
        self.user_manager.login(username="test_user", password="123456")
        result = self.user_manager.logout()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "User test_user logged out.")
        self.assertEqual(self.user_manager.logged_in_user, None)
        self.assertEqual(self.user_manager.logged_in_role, None)

    def test_logout_failure(self):
        result = self.user_manager.logout()
        self.assertEqual(result["status"], "failure")
        self.assertEqual(result["message"], "No user is currently logged in")

    @classmethod
    def tearDownClass(cls):
        cls.cur.execute("DROP TABLE IF EXISTS users;")
        cls.conn.commit()
        cls.cur.close()
        cls.conn.close()

if __name__ == "__main__":
    unittest.main()