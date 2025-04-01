from src.server import Server

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
VERSION = '0.0.1'

if __name__ == '__main__':
    server = Server(HOST, PORT, VERSION)
    server.start_server()




    
# opisać funkcje
# wypchnąc do odzielnego repo