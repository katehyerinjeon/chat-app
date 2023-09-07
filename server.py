import json
import socket


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.table = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.socket.bind((self.ip, self.port))
        self.display_status('Server up and running at {} {}'.format(self.ip, self.port))

        while True:
            message, address = self.socket.recvfrom(4096)
            message_list = message.decode('utf-8').split(' ')
            request = message_list[0]

            if request == 'reg':
                self.reg(message_list[1], address)
            elif request == 'dereg':
                self.dereg(message_list[1], address)

        self.close_socket()

    def reg(self, username, address):
        if username not in self.table:
            self.table[username] = {
                'username': username,
                'ip': address[0],
                'port': address[1],
                'isOnline': True
            }
        else:
            self.table[username]['isOnline'] = True

        self.send_ack('reg', address)
        self.broadcast_table()
        self.display_status('{} registered'.format(username))
        self.display_table()

    def dereg(self, username, address):
        self.table[username]['isOnline'] = False
        self.send_ack('dereg', address)
        self.broadcast_table()
        self.display_status('{} de-registered'.format(username))
        self.display_table()

    def send_ack(self, request, address):
        self.socket.sendto('{} ACK'.format(request).encode('utf-8'), address)

    def send_table(self, address):
        self.socket.sendto(json.dumps(self.table).encode('utf-8'), address)

    def broadcast_table(self):
        for username in self.table:
            if self.table[username]['isOnline']:
                self.send_table((self.table[username]['ip'], self.table[username]['port']))

    def display_status(self, status):
        print(status)

    def display_table(self):
        print(self.table)

    def close_socket(self):
        self.socket.close()
