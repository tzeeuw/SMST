import socket
from contextlib import closing
from server_proj.com.wol import wake_server




IP =  "yep this was definetely here during time of commit"
PORT = 42070

maintenance = False

def port_check(_IP=IP, _PORT=PORT):
    with closing(socket.socket()) as sock:
        sock.settimeout(5)
        result = sock.connect_ex((_IP, _PORT))
        return result



def status():
    result = port_check(IP, 25565)

    if result==0:
        return "online"

    elif not maintenance:
        result = port_check(IP, PORT)

        if result==0:
            return "idling"
        
        else:
            return "sleeping"
        
    else:
        return "offline"



def send_request():
    
    with closing(socket.socket()) as sock:
        packet = "Alive?"

        sock.connect((IP, PORT))
        sock.send(packet.encode())

        answer = sock.recv(1024).decode()
        print(answer)

        if answer == "yes":
            print("server is alive")

        else:
            print("server starting")


def start(prot="sleeping"):
    if prot=="idling":
        with closing(socket.socket()) as sock:
            packet = "start server"
            
            try:
                sock.connect((IP, PORT))

            except Exception as e:
                print(f"ERROR Connecting to port; exited with {e}")
                return
            
            sock.send(packet.encode())
        

    elif prot=="sleeping":
        wake_server()

        with closing(socket.socket()) as sock:
            sock.bind(("192.168.178.17", PORT))

            sock.listen()
            
            (proxy_socket, proxy_address) = sock.accept()

            message = proxy_socket.recv(1024).decode()

            if message=="wake up?":
                proxy_socket.send("yes".encode())

            else:
                proxy_socket.send("no".encode())

    


