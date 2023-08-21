import socket


class Client:
    def __init__(self, username, ip, port, server_ip, server_port):
        self.username = username
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.table = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((ip, port))

    def reg(self):
        message = 'reg {}'.format(self.username)
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def update_table(self, table):
        self.table = table
        self.display_status('>>> Table updated')

    def is_server(self, address):
        if address[0] == self.server_ip and address[1] == self.server_port:
            return True
        return False

    def display_status(self, status):
        print(status)

    def close_socket(self):
        self.socket.close()
