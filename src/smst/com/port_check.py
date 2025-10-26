import socket
from contextlib import closing
from smst.com.wol import wake_server
import threading
import json

with open('properties.json', 'r') as file:
    properties = json.load(file)


IP = properties["local_server_ip"]
BOT_IP = properties["local_bot_ip"]
PORT = int(properties["com_port"])

maintenance = False


def port_check(_IP=IP, _PORT=PORT):
    with closing(socket.socket()) as sock:
        sock.settimeout(3)
        result = sock.connect_ex((_IP, _PORT))
        return result



def status():
    result = port_check(IP, 25565)

    if maintenance:
        return "offline"

    elif result==0:
        return "online"

    elif not maintenance:
        result = port_check(IP, PORT)

        if result==0:
            return "idling"
        
        else:
            return "sleeping"
        



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


def start(prot=None):
    try:
        alive = thread.is_alive()
        print(alive)

        if alive:
            print("thread is alive")
            return
        else:
            create_thread(prot)
            thread.start()

    except NameError:
        print("thread is not yet made")
        create_thread(prot)
        thread.start()



def create_thread(prot=None):
    global thread
    thread = threading.Thread(target=start_thread, args=(prot,))


def start_thread(prot=None):
    if prot=="idling":
        with closing(socket.socket()) as sock:
            packet = "start server"
            
            try:
                sock.connect((IP, PORT))

            except Exception as e:
                print(f"ERROR Connecting to port; exited with {e}")
                return
            
            sock.send(packet.encode())
        

    # FIX: if waiting for connect but pc wont start
    elif prot=="sleeping":
        wake_server()

        with closing(socket.socket()) as sock:
            sock.bind((BOT_IP, PORT))

            sock.listen()
            
            (proxy_socket, proxy_address) = sock.accept()

            message = proxy_socket.recv(1024).decode()

            if message=="wake up?":
                proxy_socket.send("yes".encode())

            else:
                proxy_socket.send("no".encode())

    


