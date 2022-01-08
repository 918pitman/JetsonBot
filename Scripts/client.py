#!/usr/bin/python3

import socket

HOST = '143.198.161.181'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            msgout = input('To Server: ')
            if msgout == 'q':
                break
            s.sendall(msgout.encode('utf-8'))
            #data = s.recv(1024)
            #print('Received', repr(data))

if __name__ == '__main__':
    client()