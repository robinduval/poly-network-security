#C'est NUL !

from scapy.all import *
import socket

interface = "lo"
conf.checkIPaddr = False
fam, hw = socket.AF_PACKET, socket.PF_PACKET

def dhcp_callback(pkt):
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:  # DHCP Discover
        mac_addr = pkt[Ether].src
        src_ip = "10.0.0.33"
        subnet_mask = "255.255.255.0"
        offered_ip = "10.0.0.27" #My

        # Build DHCP Offer packet
        ether = Ether(src=get_if_hwaddr(interface), dst=mac_addr)
        ip = IP(src=src_ip, dst="255.255.255.255")
        udp = UDP(sport=67, dport=68)
        bootp = BOOTP(op=2, htype=1, hlen=6, yiaddr=offered_ip, siaddr=src_ip, chaddr=mac_addr)
        dhcp = DHCP(options=[("message-type", "offer"), ("subnet_mask", subnet_mask), ("server_id", src_ip), ("lease_time", 3600), "end"])
        offer = ether/ip/udp/bootp/dhcp

        sendp(offer, iface=interface, verbose=False)

sniff(iface=interface, filter="udp and (port 67 or port 68)", prn=dhcp_callback)
