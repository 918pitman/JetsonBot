import socket
import threading

def listen(sock):
    while True:
        data = sock.recv(1024)
        print('\rPeer: {}\n> '.format(data.decode()), end='')

rendezvous = ('143.198.161.181', 55555)

print('connecting to server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\nPeer Info:')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

listener = threading.Thread(target=listen, args=(sock,), daemon=True);
listener.start()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('You: ')
    sock.sendto(msg.encode(), (ip, sport))