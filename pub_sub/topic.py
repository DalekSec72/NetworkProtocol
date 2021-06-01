# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import time
import threading
from queue import Queue
from message import Message


class Topic:
    def __init__(self, name, period, client: tuple):
        self._name = name
        self._period = period
        # self._m_format = Message()
        self._last_pub = 0

        # 토픽 생성은 퍼블리셔만 할 수 있음.
        self._publisher = [client]
        self._subscriber = []

        self._message_queue = Queue()  # 토픽에 쌓인 메시지.
        self._lock = threading.Lock()

    # pub/sub list
    def append_publisher(self, publisher):
        self._publisher.append(publisher)

    def delete_publisher(self, publisher):
        self._publisher.remove(publisher)

    def append_subscriber(self, subscriber):
        self._subscriber.append(subscriber)

    def delete_subscriber(self, subscriber):
        self._subscriber.remove(subscriber)

    # message queue
    def pop_message(self):
        return self._message_queue.get()

    def put_message(self, message):
        self._message_queue.put(message)

    def is_queue_empty(self):
        return self._message_queue.empty()

    # lock
    def acquire_lock(self):
        self._lock.acquire()

    def release_lock(self):
        self._lock.release()

    # accessors
    def get_name(self):
        return self._name

    def get_publisher(self):
        return self._publisher

    def get_period(self):
        return self._period

    def get_subscriber(self):
        return self._subscriber

    def get_last_pub(self):
        return self._last_pub

    # mutators
    def set_name(self, name):
        self._name = name

    def set_period(self, period):
        self._period = period

    def set_last_pub(self):
        self._last_pub = time.time()

    # equals
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Topic):
            return self._name == other._name
        return False
