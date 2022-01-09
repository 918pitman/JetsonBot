#!/usr/bin/env python3

from threading import Thread
import socket
from typing_extensions import TypeGuard

HOST = '143.198.161.181'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def chat(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            msgin = data.decode('utf-8')
            if not data:
                print('Session ended')
                break
            else:
                print(addr,': ', msgin)


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            Thread(target=chat, args=(conn,addr)).start()


if __name__ == '__main__':
    server()