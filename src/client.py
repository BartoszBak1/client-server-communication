import socket
import json

class Client:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 65432 
        self.commands = {
                "signup": ["username", "password", "role"],
                "login": ["username", "password"],
                "send": ["recipient", "msg_content"],
            }

    def get_user_input(self):

        command = input("\nEnter the command. Type 'help' to print command list: ").strip()

        user_input = {}
        user_input['command'] = command

        if command in self.commands.keys():
            for option in self.commands[command]:
                user_input[option] = input(f">>> {option}: ").strip()

        return user_input

    def start_connection(self):
        print("Connected to the server.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                # get information from user
                msg = self.get_user_input()
                # send data to server
                s.sendall(json.dumps(msg).encode('utf-8'))
                # get server response
                server_response = json.loads(s.recv(1024).decode('utf-8'))
            
                if server_response == 'stop':
                    print("The server has been closed.")
                    break
                else:
                    if isinstance(server_response, dict):
                        print()
                        for key, value in server_response.items():
                            print(f'{key}: {value}')
                    elif isinstance(server_response, list):
                        for item in server_response:
                            print()
                            for key, value in item.items():
                                print(f'{key}: {value}')
                    else:
                        print(f'\n{server_response}')
