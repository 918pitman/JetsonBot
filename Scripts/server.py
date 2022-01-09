#!/usr/bin/env python3
import platform
import socket
from threading import Thread

HOST = '0.0.0.0'
PORT = 65432


class Peer:
    def __init__(self, conn, addr):
        self.connection = conn
        self.address = addr

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

def ConnectPeers():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        peers = []
        #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        while len(peers) < 2:
            conn, addr = server.accept()
            data = conn.recv(1024)
            msg = data.decode('utf-8')
            if msg == 'Peer':
                peers.append(Peer(conn, addr))
                print('Connected with: ', addr)
            else:
                print('Unknown client attempted to connect!')
                conn.close()
        with peers[0].connection as conn:
            msg = peers[1].address[0] + ':' + str(peers[1].address[1])
            conn.sendall(msg.encode('utf-8'))
        with peers[1].connection as conn:
            msg = peers[0].address[0] + ':' + str(peers[0].address[1])
            conn.sendall(msg.encode('utf-8'))
        
                    

            


if __name__ == '__main__':
    ConnectPeers()