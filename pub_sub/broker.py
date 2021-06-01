# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import time
import socket
import threading
from topic import Topic
from message import Message


HOST = '127.0.0.1'
PORT = 36007


global listen_sock


def log(func, cmd):
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S ")
    if not cmd:
        print(time_stamp, func)
    else:
        print(time_stamp, func, cmd)


def broker_listener():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(10)

    log('Broker started', 'Listen on: %s, %s' % listen_sock.getsockname())
    while True:
        connection, address = listen_sock.accept()

        # accept 후 Broker 객체에 커넥션 소켓과 addr 주고 init.
        broker = Broker(connection, address)

        # run 작동.
        broker.start()
        log('Accept', 'Created a new connection %s, %s' % address)

class Broker(threading.Thread):
    _topics: [Topic] = []  # 인스턴스 간 공유 필요.

    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self._connection = connection
        self._address = address

    def run(self):
        print('Broker instance init.')
        publisher = threading.Thread(target=self.publish)
        publisher.daemon = True
        publisher.start()
        print('Publisher thread init')
        while True:
            cmd = ''
            # 명령어 수신
            try:
                data = self._connection.recv(4096).rstrip()
                try:
                    cmd = data.decode('utf-8')

                except AttributeError:
                    cmd = data

                log('Received data:', cmd)
                if not cmd:
                    break

            except socket.error as err:
                log('Receive', err)

            # 명령어 파싱: '명령어 데이터'
            command, data = cmd.split()[0], cmd.split()[1:]
            if command == 'register_topic':
                self.register_topic(type=data[0], name=data[1], period=data[2])

            elif command == 'remove_topic':
                self.remove_topic(data[0])

            elif command == 'keep_alive':
                self.keep_alive(type=data[0], name=data[1])

            elif command == 'get_match_list':
                self.get_match_list(self._address)

            elif command == 'publish':
                name = data[0]
                message = Message(data[1], data[2], ' '.join(data[3:]))

                self.receive_message(name=name, message=message)

            else:
                log('Wrong command.', cmd)

    def send_data(self, data):
        if type(data) == bytes:
            self._connection.send(data)
        else:
            self._connection.send(data.encode('utf-8'))

    # topics 리스트에서 이름이 같은 topic 오브젝트를 찾아 리턴.
    def _get_topic(self, name) -> Topic:
        topic = list(filter(lambda x: x.get_name() == name, self._topics))
        return topic[0] if topic else topic  # 같은 이름을 갖는 토픽은 하나 뿐.

    # 새 토픽 등록, publish, subscribe.
    def register_topic(self, type, name, period):
        topic = self._get_topic(name)
        if type == 'publish':
            # 이미 있는 토픽에 publish.
            if topic:
                topic.append_publisher(self._address)

                return self.send_data((1, f'Publisher register complete: {name}'))
            # 없는 토픽 생성.
            else:
                new_topic = Topic(name, period, self._address)
                self._topics.append(new_topic)

                return self.send_data(f'Topic publish register complete: {name}')
        elif type == 'subscribe':
            if topic:
                topic.append_subscriber(self._address)

                return self.send_data(f'Subscriber register complete: {name}')
            else:
                self.send_data(f'No such topic: {name}')

        else:
            self.send_data(f'Wrong topic type: {type}')

    def remove_topic(self, name):
        self._topics.remove(self._get_topic(name))

        return self.send_data(f'Topic remove complete: {name}')

    def receive_message(self, name, message):
        topic = self._get_topic(name)
        topic.put_message(message)

        return self.send_data(f'Publish complete: {name}, {message}')

    def publish(self):
        while True:
            if not self._topics:
                continue

            for topic in self._topics:
                topic.acquire_lock()
                while not topic.is_queue_empty()\
                        and time.time() - topic.get_last_pub() > float(topic.get_period())\
                        and self._address in topic.get_subscriber():
                    self.send_data(f'{topic.get_name()}: {topic.pop_message()}\n')

                topic.release_lock()
                topic.set_last_pub()

    def keep_alive(self, type, name):
        topic = self._get_topic(name)
        if not topic:
            return self.send_data(f'Status: No such topic: {name}')

        if type == 'publish':
            if topic.get_publisher():
                return self.send_data('Status: Ok')
            else:
                return self.send_data(f'Status: No publisher for {name}')
        else:
            if topic.get_subscriber():
                return self.send_data('Status: Ok')
            else:
                return self.send_data(f'Status: No subscriber for {name}')

    def get_match_list(self, client):
        match = ''
        for topic in self._topics:
            if client in topic.get_publisher():
                match += 'Matched subs:\n'
                match += f'{topic.get_name()}: {topic.get_subscriber()}\n'
            if client in topic.get_subscriber():
                match += 'Matched pubs:\n'
                match += f'{topic.get_name()}: {topic.get_publisher()}\n'

        return self.send_data(match) if match else self.send_data('No matched subs')


if __name__ == '__main__':
    listen_sock = threading.Thread(target=broker_listener())
    listen_sock.start()
