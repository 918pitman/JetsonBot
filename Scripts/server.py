#!/usr/bin/env python3

import threading
import socket

MY_AS_SERVER_PORT = 9001

TIMEOUT = 120.0
BUFFER_SIZE = 4096

def get_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        print(IP)
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return bytes(IP, encoding='utf-8')

def wait_for_msg(new_connection, client_address):
    while True:
        try:
            packet = new_connection.recv(BUFFER_SIZE)
            if packet:
                msg_from_client = packet.decode('utf-8')
                client_connected_from_ip = client_address[0]
                client_connected_from_port = client_address[1]

                print("We have a client. Client advertised his local IP as:", msg_from_client)
                print(f"Although, our connection is from: [{client_connected_from_ip}]:{client_connected_from_port}")

                msg_back = bytes("SERVER registered your data. Your local IP is: " + str(msg_from_client) + " You are connecting to the server FROM: " + str(client_connected_from_ip) + ":" + str(client_connected_from_port), encoding='utf-8')
                new_connection.sendall(msg_back)
                break

        except ConnectionResetError:
            break

        except OSError:
            break

def server():
    sock = socket.socket()

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    sock.bind((get_my_local_ip().decode('utf-8'), MY_AS_SERVER_PORT))
    sock.listen(8)
    sock.settimeout(TIMEOUT)
    while True:
        try:
            new_connection, client_address = sock.accept()

            if new_connection:
                threading.Thread(target=wait_for_msg, args=(new_connection,client_address,)).start()
#               print("connected!")
#               print("")
#               print(new_connection)
#               print("")
#               print(client_address)
                msg = bytes("Greetings! This message came from SERVER as message back!", encoding='utf-8')
                new_connection.sendall(msg)
        except socket.timeout:
            pass


if __name__ == '__main__':
    server()