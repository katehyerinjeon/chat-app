class Client:
    def __init__(self, username, ip, port, server_ip, server_port):
        self.username = username
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.table = {}
