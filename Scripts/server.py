#!/usr/bin/env python3
import platform
import socket
from threading import Thread

from client import client

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
    peers = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while len(peers) <= 2:
            conn, addr = s.accept()
            with conn:
                peers.append(addr)
        print('Connected to two peers')
        print('Peer 1: ', client[0])
        print('Peer 2: ', client[1])
            


if __name__ == '__main__':
    server()