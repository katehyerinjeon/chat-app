import argparse
import sys


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
            server_port = int(args.server_args[0])

    # client mode
    if args.client_args:
        if len(args.client_args) != 4:
            raise argparse.ArgumentTypeError('For client mode, you need to provide username, server IP, server port, and client port')
        else:
            username, server_ip, server_port, client_port = args.client_args
            server_port = int(server_port)
            client_port = int(client_port)


if __name__ == '__main__':
    main()
