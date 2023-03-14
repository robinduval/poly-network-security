#!/usr/bin/env python3

from scapy.all import *
ip = "10.0.0.20"
ports = range(1, 1025)
for port in ports:
  # Envoi d'un paquet TCP SYN à l'adresse IP et port spécifiés
  response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=1, verbose=0)
  # Si le port est ouvert, le serveur renvoie un paquet SYN+ACK 0x12
  print(port)
  if response and response.haslayer(TCP) and response.getlayer(TCP).flags & 0x12:
    print(f"Port {port} ouvert")
