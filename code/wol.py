import datetime
import socket

time = datetime.datetime.now().time()


def wake_server(mac_address, port):

    # convert to hex code so that it can be send in local network
    mac_clean = mac_address.replace(":", "").replace("-", "")
    mac_byte = bytes.fromhex(mac_clean)

    # magic packet consists of a starting ff string followed by 16 x the mac address
    payload = b'\xFF'*6 + mac_byte * 16

    # broadcast packet over the local network
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        sock.sendto(payload, ("<broadcast>", port))

# early implementation to avoid turning on computer when people are sleeping
if not 1 < time.hour < 9:
    wake_server("3C-58-C2-4C-C8-EF", port=9)
else:
    print('Too late sorry mate')


if __name__ == "__main__":
    wake_server("3C-58-C2-4C-C8-EF", port=9)