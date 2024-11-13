import socket

UDP_IP =  "yep this was definetely here during time of commit"
UDP_PORT = 9090

# SOCK_DGRAM as TCP fails so UDP is required
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    message = sock.recv(1024)
    print(message.decode("utf-8"))