#!/usr/bin/python3

import platform
import socket

HOST = '143.198.161.181'
PORT = 65432


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        priv_addr = s.getsockname()
        print('Private Address is : ', priv_addr)
        # if platform.system() == 'Linux':
        #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        
        while True:
            msgout = input('To Server: ')
            if msgout == 'q':
                break
            s.sendall(msgout.encode('utf-8'))
            data = s.recv(1024)
            msgin = data.decode('utf-8')
            print('Received: ', msgin)

if __name__ == '__main__':
    client()