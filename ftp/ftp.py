# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import threading

import ftp_server
from ftp_client import FtpClient

host = '127.0.0.1'
control_port = 36007
username = 'np2021'
password = 'np2021'


def parse_command(cmd):
    return cmd.split()


def server_mode():
    print('Server mode.')
    listen_sock = threading.Thread(target=ftp_server.server_listener())
    listen_sock.start()


def client_mode():
    print('Client mode.')
    # host = input('Host:')
    # control_port = input('Port:')

    client = FtpClient()
    client.connect(host, control_port)
    client.login(username, password)

    type = 'A'

    while client:
        cmd = parse_command(input('ftp> '))
        if len(cmd) == 1:
            command = cmd[0]
            args = ''

        else:
            command = cmd[0]
            args = cmd[1]

        # NLST, ls
        if command == 'ls':
            if args:
                for line in client.NLST(args):
                    print(line)

            else:
                for line in client.NLST():
                    print(line)

        # CWD, cd
        elif command == 'cd':
            if not args:
                args = input('Change directory to: ')

            print(client.CWD(args))

        # RETR
        elif command == 'get':
            print(args)
            client.RETR(args, type)

        # TYPE
        elif command == 'type':
            if args.upper() != 'A' and args.upper() != 'I':
                print('A or I')

            else:
                type = args.upper()
                print(client.send_command(f'TYPE {type}'))

        elif command == 'ascii':
            type = 'A'
            print(client.send_command('TYPE A'))

        elif command == 'bin':
            type = 'I'
            print(client.send_command('TYPE I'))

        elif command == 'quit' or command == 'bye':
            print(client.QUIT())
            quit()


if __name__ == '__main__':
    mode = input('1: server, 2: client: ')

    if mode == '1':
        server_mode()

    elif mode == '2':
        client_mode()

    else:
        print('Press 1 or 2.')
        quit()
