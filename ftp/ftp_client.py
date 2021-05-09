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

        self.ftp.login(user=self.username, passwd=self.password)

    def nlst(self, path=''):
        return self.ftp.nlst(path)

    def cwd(self, path):
        return self.ftp.cwd(path)

    def retr(self, path, mode):
        if mode == 'A':
            with open(path, 'w') as f:
                self.ftp.retrlines("RETR " + path, f.write)

        else:
            with open(path, 'w') as f:
                self.ftp.retrbinary("RETR " + path, f.write)

    def quit(self):
        self.ftp.quit()
