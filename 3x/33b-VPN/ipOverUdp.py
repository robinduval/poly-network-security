#!/usr/bin/env python3

import os
import struct
import socket
import ssl

# Define the tunnel endpoints
tunnel_src_ip = "10.0.0.32" #ParrotVPN2
tunnel_dest_ip = "10.0.0.31" #ParrotVPN1
tunnel_src_port = 5000
tunnel_dest_port = 5001

# Create a UDP socket for the tunnel DGRAM = DATAGRAM = UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the source IP and port
sock.bind((tunnel_src_ip, tunnel_src_port))

while True:
    # Receive a packet from the tunnel
    data, addr = sock.recvfrom(1024)

    # Decrypt the packet
    decrypted_data = ssl.decrypt(data)

    # Extract the destination IP and port from the packet
    dest_ip, dest_port = extract_ip_port(decrypted_data)

    # Create a UDP socket to send the packet to the destination
    dest_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the packet to the destination
    dest_sock.sendto(decrypted_data, (dest_ip, dest_port))