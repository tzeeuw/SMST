import socket

UDP_IP =  "yep this was definetely here during time of commit"
UDP_PORT = 9090

# SOCK_STREAM so we use TCP instead of UDP, more failsave protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    sock.listen()
    conn, adr = sock.accept()
    while True:
        message = conn.recv(1024)
        if not message:
            break
        print(message.decode("utf-8"))