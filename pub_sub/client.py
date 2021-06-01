# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import socket
import threading


HOST = '127.0.0.1'
PORT = 36007

def client_send(client_socket: socket):
    while True:
        print('1. register topic, 2. remove topic, 3. keep alive, 4. get match list, 5. publish')
        command = input()
        if command == '1':
            type = input('type:')
            name = input('name:')
            period = input('period:')
            msg = f'register_topic {type} {name} {period}'

        elif command == '2':
            name = input('name:')
            msg = f'remove_topic {name}'

        elif command == '3':
            type = input('type:')
            name = input('name:')
            msg = f'keep_alive {type} {name}'

        elif command == '4':
            msg = f'get_match_list'

        elif command == '5':
            name = input('name:')
            filename = 'text'
            value = input('message:')
            filesize = len(value)
            msg = f'publish {name} {filename} {str(filesize)} {value}'

        else:
            print('Wrong command.')

        client_socket.send(msg.encode('utf-8'))


def client_receive(client_socket: socket):
    while True:
        msg = client_socket.recv(4096).decode('utf-8')
        print(msg)


def client_mode():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print('Connected to broker.')

    receive_thread = threading.Thread(target=client_receive, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=client_send, args=(client_socket, ))
    send_thread.start()


if __name__ == '__main__':
    client_mode()
