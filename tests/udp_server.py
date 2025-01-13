import socket

UDP_IP =  "yep this was definetely here during time of commit"
UDP_PORT = 42070

sock = socket.socket()

sock.bind((UDP_IP, UDP_PORT))

sock.listen()

(proxy_socket, proxy_address) = sock.accept()

data = proxy_socket.recv(1024).decode()
print(data)

proxy_socket.send("hello".encode())

proxy_socket.close()
sock.close()