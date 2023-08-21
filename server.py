import json
import socket


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.table = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((ip, port))

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
        self.send_table(address)

    def send_ack(self, request, address):
        self.socket.sendto('{} ACK'.format(request).encode('utf-8'), address)

    def send_table(self, address):
        self.socket.sendto(json.dumps(self.table).encode('utf-8'), address)

    def broadcast_table(self):
        for username in self.table:
            if self.table[username]['isOnline']:
                self.send_table((self.table[username]['ip'], self.table[username]['port']))

    def close_socket(self):
        self.socket.close()
