import json
import socket
from threading import Thread


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

        user_input_thread = Thread(target=self.user_input)
        user_input_thread.start()

        print('>>>', end=' ')

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
                            self.display_status('Welcome! You are registered.')
                        elif message_list[1] == 'already_online':
                            self.display_status('You are already online.')
                    elif request == 'dereg':
                        if message_list[1] == 'ACK':
                            self.display_status('You are offline. Goodbye.')
                        elif message_list[1] == 'already_offline':
                            self.display_status('You are already offline. Register to be online.')

            # message received from another client
            else:
                for username in self.table:
                    if address[0] == self.table[username]['ip'] and address[1] == self.table[username]['port']:
                        self.display_status('{}: {}'.format(username, message.decode('utf-8')))

        self.close_socket()

    def user_input(self):
        while True:
            user_input = input()
            input_list = user_input.split(' ')
            request = input_list.pop(0)

            if request == 'reg':
                self.reg()
                print('>>>', end=' ')
            elif request == 'dereg':
                self.dereg()
                print('>>>', end=' ')
            elif request == 'send':
                username = input_list.pop(0)
                message = ' '.join(input_list)
                print('>>>', end=' ')
                self.send(username, message)

    def reg(self):
        message = 'reg {}'.format(self.username)
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def dereg(self):
        message = 'dereg {}'.format(self.username)
        self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def send(self, username, message):
        if username not in self.table:
            self.display_status('Username {} not found. Try again'.format(username))
        else:
            recipient = self.table[username]
            if recipient['isOnline']:
                self.socket.sendto(message.encode('utf-8'), (recipient['ip'], recipient['port']))
            else:
                self.socket.sendto('{} {}'.format(username, message).encode('utf-8'), (self.server_ip, self.server_port))

    def send_ack(self, request, address):
        self.socket.sendto('{} ACK'.format(request).encode('utf-8'), address)

    def update_table(self, table):
        self.table = table
        self.display_status('Table updated.')
        self.display_status(self.table)

    def is_server(self, address):
        if address[0] == self.server_ip and address[1] == self.server_port:
            return True
        return False

    def display_status(self, status):
        print('{}\n>>> '.format(status), end='')

    def close_socket(self):
        self.socket.close()
