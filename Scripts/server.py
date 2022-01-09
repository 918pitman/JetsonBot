#!/usr/bin/env python3
import platform
import socket
from threading import Thread

HOST = '0.0.0.0'
PORT = 65432

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
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            Thread(target=chat, args=(conn,addr)).start()


if __name__ == '__main__':
    server()