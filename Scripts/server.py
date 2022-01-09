#!/usr/bin/env python3

from threading import Thread
import socket

HOST = '143.198.161.181'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def chat(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            msgin = data.decode('utf-8')
            print(addr,': ', msgin)
            if not data:
                break



def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        chat(conn, addr)
            



if __name__ == '__main__':
    server()