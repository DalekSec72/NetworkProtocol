# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

from ftp_client import FtpClient


host = '127.0.0.1'
control_port = 36007
username = 'np2021'
password = 'np2021'


def parse_command(cmd):
    return cmd.split()


if __name__ == '__main__':
    mode = input('1: server, 2: client: ')

    if mode == '1':
        print('Server mode.')


    elif mode == '2':
        print('Client mode.')
        # host = input('Host:')
        # control_port = input('Port:')

        client = FtpClient()
        client.connect(host, control_port)
        client.login(username, password)

        mode = 'A'
        is_passive = True

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
                    for line in client.nlst(args):
                        print(line)

                else:
                    for line in client.nlst():
                        print(line)

            # CWD, cd
            elif command == 'cd':
                if not args:
                    args = [input('Change directory to: ')]

                client.cwd(args)

            # RETR
            elif command == 'get':
                print(args)
                client.retr(args, mode)

            # TYPE
            elif command == 'TYPE':
                if args != 'A' or args != 'I':
                    print('A or I')

                else:
                    mode = args

            elif command == 'ascii':
                mode = 'A'

            elif command == 'bin':
                mode = 'I'

            elif command == 'quit' or command == 'bye':
                client.quit()

    else:
        print('Press 1 or 2.')
        quit()
