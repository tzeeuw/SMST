import socket
from contextlib import closing
import time
import pyshark


# checks if port is open or not
def port_check():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        result = sock.connect_ex(('192.168.178.17', 25565))
        return result

# filters mean only unique tcp requests to a port will be captured and retransmissions/icmp (return messages) will be ignored
capture = pyshark.LiveCapture('Ethernet', display_filter="tcp.port == 25565 and not tcp.analysis.retransmission and not icmp")
for packet in capture.sniff_continuously():
    print(f'Just arrived: {packet}')
