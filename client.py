import json
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

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.reg()

        while True:
            message, address = self.socket.recvfrom(4096)
            # message received from server
            if self.is_server(address):
                try:
                    table = json.loads(message.decode('utf-8'))
                    self.update_table(table)

                except json.decoder.JSONDecodeError:
                    message_list = message.decode('utf-8').split(' ')
                    request = message_list[0]

                    if request == 'reg':
                        if message_list[1] == 'ACK':
                            self.display_status('>>> Welcome! You are registered.')
                    elif request == 'dereg':
                        if message_list[1] == 'ACK':
                            self.display_status('>>> Goodbye.')

            # message received from another client
            else:
                pass

        self.close_socket()

    def reg(self):
        message = 'reg {}'.format(self.username)
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def dereg(self):
        message = 'dereg {}'.format(self.username)
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def update_table(self, table):
        self.table = table
        self.display_status('>>> Table updated.')
        self.display_table()

    def is_server(self, address):
        if address[0] == self.server_ip and address[1] == self.server_port:
            return True
        return False

    def display_status(self, status):
        print(status)

    def display_table(self):
        print(self.table)

    def close_socket(self):
        self.socket.close()
