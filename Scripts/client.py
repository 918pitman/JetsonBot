#!/usr/bin/python3

import platform
import socket

HOST = '143.198.161.181'
PORT = 65432


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # if platform.system() == 'Linux':
        #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.connect((HOST, PORT))
        priv_addr = s.getsockname()
        print('Private Address is : ', priv_addr)
        s.sendall('Peer'.encode('utf-8'))
        data = s.recv(1024)
        resp = data.decode('utf-8')
        if 'First' in resp:
            print('I connected to the server first!')
        elif 'Second' in resp:
            print('I connected to the server second!')
        else:
            print('Access Denied')
        

if __name__ == '__main__':
    client()