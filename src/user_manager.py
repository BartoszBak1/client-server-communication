from src.user import User

class UserManager():

    def __init__(self, database) -> None:
        self.db = database
        self.logged_in_user = None
        self.logged_in_role = None


    def create_account(self, **kwargs):
        """Create account for new user. Username must be unique. 

        Args:
            username (str): name of user
            password (str): password
            role (str): role (admin or user)

        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        role = kwargs.get('role')

        if role not in ['user', 'admin']:
            return {"status": "failure", 'message': 'Wrong role. Select user or admin.'}
        
        data = self.db.load_data(self.db.database_path, self.db.file_users)

        if self.db.check_if_user_exist(data, username):
            return {"status": "failure", "message": f"User with that name already exist."}
        else:
            user = User(username, password, role)
            data.append(user.__dict__)
            self.db.save_data(self.db.database_path, self.db.file_users, data)
            return {"status": "success", "message": f"You have created new account named {username}."}

    def login(self, **kwargs):
        """Log in to an account. 

        Args:
            username (str): name of user
            password (str): password

        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        data = self.db.load_data(self.db.database_path, self.db.file_users)
        
        if self.logged_in_user is not None:
            return {"status": "failure", "message": f"You are logged in as {self.logged_in_user}."}

        user = self.db.get_user_data(data, username)
        
        if  self.db.check_credentials(user, username, password):
            self.logged_in_user = username
            self.logged_in_role = user['role']
            return {"status": "success", "message": f"User {username} logged in."}
        else:
            return {"status": "failure", "message": f"Invalid username or password."}

    def logout(self, **kwargs):
        """Log out of an account. 

        Args:
            username (str): name of user
            password (str): password

        Returns:
            dict: Dictionary with status of job (failure or success) and message.
        """
        if self.logged_in_user: 
            username = self.logged_in_user
            self.logged_in_user = None
            self.logged_in_role = None
            return {"status": "success","message": f"User {username} logged out."}
        else:
            return {"status": "failure", "message": "No user is currently logged in"}
        
    def is_logged_in(self):
        """Check if any user is logged in. 

        Returns:
            bool: True/False
        """
        return self.logged_in_user is not None
    
    def get_logged_in_user(self):
        """Get logged in username. 

        Returns:
            str: username
        """
        return self.logged_in_user
    
    def get_logged_in_role(self):
        """Get logged in user's role. 

        Returns:
            str: role
        """
        return self.logged_in_role