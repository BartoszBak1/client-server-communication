import unittest
import json
import os
from src.user_manager import UserManager
from src.database import Database

class UserTests(unittest.TestCase):

    def setUp(self):
        self.test_db_path = "tests/tests_data"
        self.file_name = "users.json"
        with open(os.path.join(self.test_db_path, self.file_name), 'w') as f:
            json.dump([],f)

        self.db = Database(self.test_db_path) 
        self.user_manager = UserManager(self.db)

        self.user_credentials = {'username': 'test_user', 'password': '123456', 'role': 'user'}

    def test_create_account_success(self):

        result = self.user_manager.create_account(**self.user_credentials)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], "You have created new account named test_user.")

        data = self.db.load_data(self.test_db_path, self.file_name)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'test_user')

    def test_create_account_failure(self):

        self.user_manager.create_account(**self.user_credentials)
        result = self.user_manager.create_account(**self.user_credentials)

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], "User with that name already exist.")

    def test_create_account_wrong_role(self):

        result = self.user_manager.create_account(username = 'test_user', password = '123456', role = 'xxxx')

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], "Wrong role. Select user or admin.")     

    def test_login_success(self):

        self.user_manager.create_account(**self.user_credentials)

        result = self.user_manager.login(username = 'test_user', password = '123456')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'User test_user logged in.')
        self.assertEqual(self.user_manager.logged_in_user, 'test_user')
        self.assertEqual(self.user_manager.logged_in_role, 'user')

    def test_login_wrong_name(self):

        self.user_manager.create_account(**self.user_credentials)

        result = self.user_manager.login(username = 'wrong_name', password = '123456')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Invalid username or password.') 
        self.assertEqual(self.user_manager.logged_in_user, None)

    def test_login_wrong_password(self):

        self.user_manager.create_account(**self.user_credentials)

        result = self.user_manager.login(username = 'test_user', password = 'wrong_password')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'Invalid username or password.')
        self.assertEqual(self.user_manager.logged_in_user, None)

    def test_login_already_login(self):
        
        self.user_manager.create_account(**self.user_credentials)
        self.user_manager.login(username = 'test_user', password = '123456')

        result = self.user_manager.login(username = 'test_user', password = '123456')
        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'You are logged in as test_user.')   

    def test_logout_success(self):

        self.user_manager.create_account(**self.user_credentials)
        self.user_manager.login(username = 'test_user', password = '123456')

        result = self.user_manager.logout()

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'User test_user logged out.')
        self.assertEqual(self.user_manager.logged_in_user, None)
        self.assertEqual(self.user_manager.logged_in_role, None)

    def test_logout_failure(self):
        
        result = self.user_manager.logout()

        self.assertEqual(result['status'], 'failure')
        self.assertEqual(result['message'], 'No user is currently logged in')       



    def tearDown(self):
        if os.path.exists(os.path.join(self.test_db_path, self.file_name)):
            os.remove(os.path.join(self.test_db_path, self.file_name))
# testy

    # urzykownicy
        # dane do logowania i tworzenia urzytkowników wywalić do jsona

if __name__ == "__main__":
    unittest.main()
        