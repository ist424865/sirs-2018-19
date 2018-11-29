"""
Host search inside a network
"""

import socket
import nmap
import ifaddr


# Returns the ip of the current machine
# It just returns the source address if some datagram is sent (in this case not)
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        s.close()
        return s.getsockname()[0]
    except socket.error:
        return "127.0.0.1"


# Find all IP addresses of the computer
def get_ip_addresses():
    networks = list()
    adapters = ifaddr.get_adapters()

    for adapter in adapters:
        for ip in adapter.ips:
            networks.append("%s/%s" % (ip.ip, ip.network_prefix))

    return networks


# Get open UDP ports of given host
def scan_udp_ports(host):

    nm = nmap.PortScanner()
    nm.scan(host, arguments='sudo -n -sU')

    ports = list()

    # Search only for UDP ports
    try:
        udp_ports = nm[host]['udp'].keys()

        # Only add open ports
        for port in udp_ports:
            state = nm[host]['udp'][port]['state']
            if state == 'open':
                ports.append(port)
    except KeyError:
        # No UDP ports found
        print("No UDP ports found")

    return ports


# Search hosts on given network address (example: 192.168.1.0/24)
def search_hosts(address):
    hosts = list()

    nm = nmap.PortScanner()
    nm.scan(hosts=address, arguments='-sP')

    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            hosts.append(host)

    return hosts