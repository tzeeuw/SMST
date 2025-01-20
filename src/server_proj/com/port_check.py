import socket
from contextlib import closing
from server_proj import wol



# filters mean only unique tcp requests to a port will be captured and retransmissions/icmp (return messages) will be ignored
# capture = pyshark.LiveCapture('Ethernet', display_filter="tcp.port == 25565 and not tcp.analysis.retransmission and not icmp")
# first_call = False

# for packet in capture.sniff_continuously():
#     print(packet.ip.src)

#     if not first_call:
#         ip_address = packet.ip.src
#         recieve_time = datetime.datetime.now()
#         first_call = True

#     elif packet.ip.src == ip_address:
#         print('test')
#         first_call = False
#         break

#     elif datetime.datetime.now() - recieve_time > 30:
#         first_call = False
#         ip_address = 0
    
#     print(ip_address)


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
        return "Online"

    elif not maintenance:
        result = port_check(IP, PORT)

        if result==0:
            return "Idling"
        
        else:
            return "Sleeping"
        
    else:
        return "Offline"


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

if __name__ == "__main__":
    send_request()
