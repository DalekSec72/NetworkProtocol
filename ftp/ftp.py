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
        # server
        print('Server mode.')

    elif mode == '2':
        print('Client mode.')
        # host = input('Host:')
        # control_port = input('Port:')

        client = FtpClient()
        client.connect(host, control_port)
        client.login(username, password)

        while client:
            command = parse_command(input('ftp> '))
            if len(command) == 1:
                command = command[0]
                args = ''

            else:
                command = command[0]
                args = command[1:]

            # NLST, ls
            if command == 'ls':
                if args:
                    for line in client.nlst(args[0]):
                        print(line)

                else:
                    for line in client.nlst():
                        print(line)

            # CWD, cd
            elif command == 'cd':
                if not args[0]:
                    args[0] = input('Change directory to: ')

                client.cwd(args[0])

            elif command == 'get':
                pass


    else:
        print('Press 1 or 2.')
        quit()
