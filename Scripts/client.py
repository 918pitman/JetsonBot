#!/usr/bin/python3

import sys
import socket
import time
import threading

SERVER_IP = '143.198.161.181'
SERVER_PORT = 9001
# We don't want to establish a connection with a static port. Let the OS pick a random empty one.
#MY_AS_CLIENT_PORT = 8510

TIMEOUT = 3
BUFFER_SIZE = 4096

def get_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print(IP)
    return bytes(IP, encoding='utf-8')

def try_connect(sock):
        try:
            sock.connect((SERVER_IP, SERVER_PORT))
        except ConnectionRefusedError:
            print(f"Can't connect to the SERVER IP [{SERVER_IP}]:{SERVER_PORT} - does the server alive? Sleeping for a while...")
            time.sleep(1)
        except OSError:
            #print("Already connected to the server. Kill current session to reconnect...")
            pass

def constantly_try_to_connect(sock):
    while True:
        try_connect(sock)

def client():
    sock = socket.socket()

    # The following line won't work on Windows.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.settimeout(TIMEOUT)
    try_connect(sock)
    #threading.Thread(target=constantly_try_to_connect, args=(sock,)).start()

    while True:
        try:
            packet = sock.recv(BUFFER_SIZE)

            if packet:
                print(packet)
                sock.sendall(get_my_local_ip())

        except OSError:
            pass

if __name__ == '__main__':
    client()