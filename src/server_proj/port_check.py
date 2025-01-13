import socket
from contextlib import closing
import time
import datetime
from server_proj import wol
import pyshark


# checks if port is open or not
def port_check():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        result = sock.connect_ex(('192.168.178.17', 25565))
        return result

# filters mean only unique tcp requests to a port will be captured and retransmissions/icmp (return messages) will be ignored
capture = pyshark.LiveCapture('Ethernet', display_filter="tcp.port == 25565 and not tcp.analysis.retransmission and not icmp")
first_call = False

for packet in capture.sniff_continuously():
    print(packet.ip.src)

    if not first_call:
        ip_address = packet.ip.src
        recieve_time = datetime.datetime.now()
        first_call = True

    elif packet.ip.src == ip_address:
        print('test')
        first_call = False
        break

    elif datetime.datetime.now() - recieve_time > 30:
        first_call = False
        ip_address = 0
    
    print(ip_address)



def send_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = "Alive".encode("utf-8")
    sock.sendto(packet, ( "yep this was definetely here during time of commit", "42070"))
