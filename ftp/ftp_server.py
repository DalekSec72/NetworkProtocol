# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import os
import socket
import threading
import time

PWD = os.getcwd()
HOST = '127.0.0.1'
PORT = 21

global listen_sock


def log(func, cmd):
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S ")
    if not cmd:
        print(time_stamp, func)
    else:
        print(time_stamp, func, cmd)


def server_listener():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(10)

    log('Server started', 'Listen on: %s, %s' % listen_sock.getsockname())
    while True:
        connection, address = listen_sock.accept()

        # accept 후 FtpServer 객체에 커맨드소켓과 addr 주고 init.
        server = FtpServer(connection, address)

        # 서버 run 작동.
        server.start()
        log('Accept', 'Created a new connection %s, %s' % address)


class FtpServer(threading.Thread):
    # 커맨드소켓과 addr 받아 서버객체 생성.
    def __init__(self, comm_sock, address):
        threading.Thread.__init__(self)
        self.pasv_mode = False
        self.pwd = PWD
        self.comm_sock = comm_sock
        self.address = address

        # 실습을 위한 유저
        self.default_user = 'np2021'
        self.default_user_pw = 'np2021'

    def run(self):
        # 연결되면 웰컴메시지 송신.
        self.send_welcome()
        while True:
            # 명령어 수신
            try:
                data = self.comm_sock.recv(1024).rstrip()
                try:
                    cmd = data.decode('utf-8')

                except AttributeError:
                    cmd = data

                log('Received data', cmd)
                if not cmd:
                    break

            except socket.error as err:
                log('Receive', err)

            # 명령어 파싱, 실행할 함수와 argument 인식
            try:
                # 명령어는 4자를 넘지 않고, 그 이하는 공백 제거.
                command, args = cmd[:4].strip().upper(), cmd[4:].strip() or None

                func = getattr(self, command)
                func(args)

            except AttributeError as err:
                log('Receive', err)

    # 데이터 전송시 데이터소켓 생성
    def start_datasock(self):
        log('start_datasock', 'Opening data channel')
        try:
            self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 패시브
            if self.pasv_mode:
                self.data_sock, self.address = self.server_sock.accept()

            # 액티브, 서버가 클라이언트에 접속 시도
            else:
                self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_sock.connect((self.data_sock_addr, self.data_sock_port))

        except socket.error as err:
            log('start_datasock', err)
            self.send_command("425 Can't open data connection.")

    # 데이터소켓 close
    def stop_datasock(self):
        log('stop_datasock', 'Closing data channel')
        try:
            self.data_sock.close()
            if self.pasv_mode:
                self.server_sock.close()

        except socket.error as err:
            log('stop_datasock', err)

    # 커맨드소켓으로 전송
    def send_command(self, cmd):
        self.comm_sock.send(cmd.encode('utf-8'))

    def send_welcome(self):
        self.send_command('220 Service ready for new user.\r\n')

    # 데이터소켓으로 전송
    def send_data(self, data):
        if type(data) == bytes:
            self.data_sock.send(data)
        else:
            self.data_sock.send(data.encode('utf-8'))

    # USER
    def USER(self, user):
        log("USER", user)
        if not user:
            self.send_command('501 Syntax error in parameters or arguments.\r\n')

        else:
            self.send_command('331 User name okay, need password.\r\n')
            self.username = user

    # PASS
    def PASS(self, passwd):
        log("PASS", passwd)
        if not passwd:
            self.send_command('501 Syntax error in parameters or arguments.\r\n')

        elif not self.username:
            self.send_command('503 Bad sequence of commands.\r\n')

        # 유저와 패스워드를 잘 받았다면
        else:
            self.passwd = passwd

            # 등록된 유저 정보와 비교.
            if self.default_user != self.username or self.default_user_pw != self.passwd:
                self.send_command('530 Not logged in.')

            else:
                self.send_command('230 User logged in, proceed. Logged out if appropriate.\r\n')

    # 아스키, 바이너리
    def TYPE(self, type):
        log('TYPE', type)
        self.mode = type
        if self.mode == 'I':
            self.send_command('200 Type set to I.\r\n')

        elif self.mode == 'A':
            self.send_command('200 Type set to A.\r\n')

        else:
            self.send_command('501 Syntax error in parameters or arguments.\r\n')

    # 패시브모드
    def PASV(self, cmd):
        log("PASV", cmd)
        self.pasv_mode = True
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_sock.bind((HOST, 0))
        self.server_sock.listen(10)
        addr, port = self.server_sock.getsockname()
        print(addr, port)

        self.send_command('227 Entering Passive Mode (%s,%u,%u).\r\n' %
                          (','.join(addr.split('.')), port >> 8 & 0xFF, port & 0xFF))

    def PORT(self, cmd):
        log("PORT: ", cmd)
        if self.pasv_mode:
            self.server_sock.close()
            self.pasv_mode = False

        # 커맨드가 PORT h1, h2, h3, h4, p1, p2로 들어옴
        # l = h1부터 p2 콤마로 스플릿
        l = cmd[5:].split(',')

        # 호스트 주소
        self.data_sock_addr = '.'.join(l[:4])

        # 포트, p1 * 256 + p2
        self.data_sock_port = (int(l[4]) << 8) + int(l[5])
        self.send_command('200 Get port.\r\n')

    # NLST, ls 대응, path로 받은 디렉토리 파일 나열.
    def NLST(self, path=None):
        # ls만 오면 현재 디렉토리에 대해...
        print(self.pwd)
        if not path:
            pathname = os.path.abspath(os.path.join(self.pwd, '.'))

        elif path.startswith(os.path.sep):
            pathname = os.path.abspath(path)

        else:
            pathname = os.path.abspath(os.path.join(self.pwd, path))

        log('NLST', pathname)

        if not os.path.exists(pathname):
            self.send_command('550 Requested action not taken. File unavailable (e.g., file not found, no access).\r\n')

        else:
            self.send_command('150 File status okay; about to open data connection.\r\n')
            self.start_datasock()
            for line in os.listdir(self.pwd):
                self.send_data(line + '\r\n')

            self.stop_datasock()
            self.send_command('226 Closing data connection. Requested file action successful.\r\n')

    # CWD
    def CWD(self, path):
        pathname = path.endswith(os.path.sep) and path or os.path.join(self.pwd, path)
        log('CWD', pathname)

        # 없는 디렉토리면 에러.
        if not os.path.exists(pathname) or not os.path.isdir(pathname):
            self.send_command('550 Requested action not taken. File unavailable (e.g., file not found, no access).\r\n')
            return

        self.pwd = pathname
        self.send_command('250 Requested file action okay, completed.\r\n')

    # cd .. 의 경우.
    def CDUP(self, path):
        pathname = '\\'.join(self.pwd.split('\\')[:-1])
        log('CDUP', pathname)

        if not os.path.exists(pathname) or not os.path.isdir(pathname):
            self.send_command('550 Requested action not taken. File unavailable (e.g., file not found, no access).\r\n')
            return

        self.pwd = pathname
        self.send_command('250 Requested file action okay, completed.\r\n')

    # RETR, 파일 전송.
    def RETR(self, filename):
        pathname = os.path.join(self.pwd, filename)
        log('RETR', pathname)

        if not os.path.exists(pathname):
            return

        # 바이너리, 아스키.
        try:
            if self.mode == 'I':
                file = open(pathname, 'rb')
            else:
                file = open(pathname, 'r')

        except OSError as err:
            log('RETR', err)

        self.send_command('150 File status okay; about to open data connection.\r\n')

        # 데이터소켓 열고 파일 읽어 보내기.
        self.start_datasock()
        while True:
            data = file.read(1024)
            if not data:
                break
            self.send_data(data)

        file.close()
        self.stop_datasock()
        self.send_command('226 Closing data connection. Requested file action successful.\r\n')

    # QUIT
    def QUIT(self, arg):
        log('QUIT', arg)
        self.send_command('221 Service closing control connection.\r\n')
