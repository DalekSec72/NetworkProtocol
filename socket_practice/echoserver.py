# -*- coding: utf-8 -*-

# 2020 HYU. CSE
# Taehun Kim <th6424@gmail.com>

from socket import *

buffer_size = 1024


def server_mode():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', 36007))

    server_socket.listen(5)

    connection_socket, addr = server_socket.accept()
    print(f'Connected with {addr}.')

    while True:
        msg = connection_socket.recv(buffer_size).decode('utf-8')
        if msg:
            print('Client: ', msg)

            connection_socket.send(msg.encode('utf-8'))
            print('Server: ', msg)


def client_mode():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 36007))
    print('Connected to server.')

    while True:
        msg = input('Client: ')
        client_socket.send(msg.encode('utf-8'))

        print('Server: ', client_socket.recv(buffer_size).decode('utf-8'))


if __name__ == '__main__':
    while True:
        mode = input('1. Server, 2. Client: ')

        if mode == '1':
            server_mode()

        elif mode == '2':
            client_mode()

        else:
            print('Press 1 or 2.')
            exit()