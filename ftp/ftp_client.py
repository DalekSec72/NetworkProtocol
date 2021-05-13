# -*- coding: utf-8 -*-

# 2021 HYU. CSE
# Taehun Kim <th6424@gmail.com>

import ftplib


class FtpClient:
    def __init__(self):
        self.host = None
        self.control_port = None

        self.username = None
        self.password = None

        self.ftp = None

    def connect(self, host, port):
        self.host = host
        self.control_port = port

        self.ftp = ftplib.FTP(self.host)
        print(self.ftp.getwelcome())

    def login(self, user, pw):
        self.username = user
        self.password = pw

        # return self.ftp.login(user=self.username, passwd=self.password)

        # 중간에 331 응답을 받기 위해 일부러 쪼갬.
        print(self.send_command(f'USER {self.username}'))
        print(self.send_command(f'PASS {self.password}'))

    def send_command(self, cmd):
        return self.ftp.sendcmd(cmd)

    def NLST(self, path=''):
        return self.ftp.nlst(path)

    def CWD(self, path):
        return self.ftp.cwd(path)

    def RETR(self, path, mode):
        if mode == 'A':
            with open(path, 'w') as f:
                self.ftp.retrlines("RETR " + path, f.write)

        else:
            with open(path, 'wb') as f:
                self.ftp.retrbinary("RETR " + path, f.write)

    def QUIT(self):
        return self.ftp.quit()
