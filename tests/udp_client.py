import socket

UDP_IP =  "yep this was definetely here during time of commit"
UDP_PORT = 42070

# SOCK_DGRAM as TCP fails so UDP is required
sock = socket.socket()

sock.connect((UDP_IP, UDP_PORT))
sock.send("faggot".encode())

data = sock.recv(1024).decode()

print(data)

sock.close()
