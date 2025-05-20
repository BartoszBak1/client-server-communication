import socket
import json 
from datetime import datetime
from src.user_manager import UserManager
from src.message_manager import MessageManager
from src.database import Database

class Server:
    def __init__(self, host, port, version, config) -> None:
        self.host = host
        self.port = port
        self.version = version
        self.config = config
        self.start_time = datetime.now()
        self.db = Database(self.config)
        self.user_manager = UserManager(self.db)
        self.message_manager = MessageManager(self.db, self.user_manager)
        self.options = {
            "uptime": self.uptime,
            "info": self.info,
            "help": self.help,
            "stop": self.stop,
            "signup": self.user_manager.create_account,
            "login": self.user_manager.login,
            "logout": self.user_manager.logout,
            "send": self.message_manager.send_msg_to_recipient,
            "read": self.message_manager.read_msg}
        self.commands = {
            "uptime": "Returns the server's lifetime.",
            "info": "Returns the server's version number and date of creation.",
            "help": "Returns a list of available commands.",
            "stop": "Stop the server and the client simultaneously.",
            "signup": "Create a new account",
            "login": "Log in.",
            "logout": "Log out.",
            "send": "Send message.",
            "read": "Read message."
               }
        
        
    def send_msg(self, conn, msg, code ='utf-8'):
        conn.sendall(msg.encode(code))

    def receive_msg(self, conn, code='utf-8'):
        return conn.recv(1024).decode(code)

    def start_server(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print(f"Connected by {addr}")

                while True:
                    data = self.receive_msg(conn)
                    if not data:
                        break

                    request = json.loads(data)
                    command = request.get('command')

                    try:
                        answer = self.options[command](**request)
                        self.send_msg(conn, msg = json.dumps(answer))
                    except KeyError:
                        self.send_msg(conn, msg = json.dumps('Wrong command')) 
                            

    def uptime(self, *args, **kwargs):

        return {"uptime": str(datetime.now() - self.start_time)}
    
    def info(self, *args, **kwargs):

        return {"version": self.version, 
                "stat_time": self.start_time.isoformat()}
    
    def stop(self, *args, **kwargs):
        
        return 'stop'

    def help(self, *args, **kwargs):
        
        return self.commands