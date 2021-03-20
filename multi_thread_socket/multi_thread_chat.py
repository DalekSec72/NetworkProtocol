# -*- coding: utf-8 -*-

# 2020 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import threading
from concurrent.futures import ThreadPoolExecutor
from socket import *
from queue import Queue
from typing import Tuple, List

# 전역 lock.
lock = threading.Lock()

# 공용 메시지 버퍼.
message_buffer = Queue()

KILL = 0
buffer_size = 1024


def server_send(clients: List[socket],):
    global message_buffer
    print('Server sender started.')

    while True:
        if not message_buffer.empty():
            # 버퍼 락
            lock.acquire()
            data = message_buffer.get()
            lock.release()

            # kill 신호 들어오면 스레드 종료.
            if data == KILL:
                break

            # 각 클라이언트(송신자 제외)에 메시지 전파.
            print(data[0:])
            for client, _ in clients:
                try:
                    if client != data[0][0]:
                        msg = data[0][1] + ': ' + data[1]
                        client.send(msg.encode('utf-8'))

                # 커넥션 에러(수신자 없음) 발생 시 패스.
                except ConnectionError as e:
                    print(e)
                    continue


def server_receive(client: Tuple[socket, str]):
    global message_buffer
    print('Server receiver started.')

    while True:
        try:
            data = [client, client[0].recv(buffer_size).decode('utf-8')]
            if data[1]:
                lock.acquire()
                message_buffer.put(data)
                lock.release()

        # 커넥션 에러 발생 시 스레드 종료.
        except ConnectionError:
            print('Terminate receiver thread.', client[1])
            break


def client_send(client_socket: socket):
    while True:
        msg = input().encode('utf-8')
        client_socket.send(msg)


def client_receive(client_socket: socket):
    while True:
        msg = client_socket.recv(buffer_size).decode('utf-8')
        print(msg)


def server_mode():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', 36007))

    # 접속제한 10개.
    server_socket.listen(10)

    # 클라이언트 커넥션 소켓 리스트.
    clients = []

    # 수신 스레드 목록, 제한 10개.
    receivers = []
    with ThreadPoolExecutor(10) as executor:
        while True:
            # 연결 끊긴 클라이언트 체크.
            if clients:
                print('Detecting dead client...')
                dead_clients = []
                for i in range(0, len(clients)):
                    print(f'Checking client number {i}.')
                    try:
                        # 테스트 바이트 전송.
                        clients[i][0].send(bytes(1))

                    except ConnectionError:
                        print(f'Dead client detected. {i}')
                        dead_clients.append(i)
                        continue

                for dead_client in sorted(dead_clients, reverse=True):
                    print('Delete dead client.', dead_client)
                    del clients[dead_client]

                print('Detecting finished.', print(clients))

            # accept 후 클라이언트 리스트에 추가.
            connection_socket, addr = server_socket.accept()
            clients.append((connection_socket, str(addr)))
            print(f'Connected with {addr}. {len(clients)} clients connected.')

            # 수신 스레드 생성.
            print('Server receiver start.')
            receiver = executor.submit(server_receive, (connection_socket, str(addr)))
            receivers.append(receiver)

            # 클라이언트 늘어나면 송신 스레드에 클라이언트 정보를 다시 주고 새로 생성.
            if len(clients) > 1 and send_thread.is_alive():
                message_buffer.put(KILL)
                print('Server sender restart.')

            # 첫 클라이언트 연결 시.
            else:
                print('Server sender start.')

            send_thread = threading.Thread(target=server_send, args=(clients,))
            send_thread.start()


def client_mode():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 36007))
    print('Connected to server.')

    send_thread = threading.Thread(target=client_send, args=(client_socket, ))
    send_thread.start()

    receive_thread = threading.Thread(target=client_receive, args=(client_socket, ))
    receive_thread.start()


if __name__ == '__main__':
    mode = input('1. Server, 2. Client: ')

    if mode == '1':
        server_mode()

    elif mode == '2':
        client_mode()

    else:
        print('Press 1 or 2.')
        exit()
