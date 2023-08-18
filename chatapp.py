import argparse
import socket
import sys
from client import Client
from server import Server


def check_port_range(port_str):
    port_int = int(port_str)
    if port_int < 1024 or port_int > 65535:
        raise argparse.ArgumentTypeError('Server port must be in the range 1024-65535')
    return port_int


def main():
    if len(sys.argv) < 2:
        raise argparse.ArgumentTypeError('Specify either server(-s) or client(-c) mode')

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', nargs='+', dest='server_args', type=check_port_range)
    parser.add_argument('-c', nargs='+', dest='client_args')
    args = parser.parse_args()

    # server mode
    if args.server_args:
        if len(args.server_args) != 1:
            raise argparse.ArgumentTypeError('For server mode, you need to provide the server port')
        else:
            port = int(args.server_args[0])
            host_name = socket.gethostname()
            ip = socket.gethostbyname(host_name)
            server = Server(ip, port)

    # client mode
    if args.client_args:
        if len(args.client_args) != 4:
            raise argparse.ArgumentTypeError('For client mode, you need to provide username, server IP, server port, and client port')
        else:
            username, port, server_ip, server_port = args.client_args
            port = int(port)
            server_port = int(server_port)
            host_name = socket.gethostname()
            ip = socket.gethostbyname(host_name)
            client = Client(username, ip, port, server_ip, server_port)


if __name__ == '__main__':
    main()
