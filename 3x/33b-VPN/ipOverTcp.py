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

# Create a TCP socket for the tunnel
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the source IP and port
sock.bind((tunnel_src_ip, tunnel_src_port))

# Listen for incoming connections
sock.listen(1)

while True:
    # Accept incoming connection from the tunnel client
    tunnel_client, addr = sock.accept()

    # Receive a packet from the tunnel client
    data = tunnel_client.recv(1024)

    # Decrypt the packet
    decrypted_data = ssl.decrypt(data)

    # Extract the destination IP and port from the packet
    dest_ip, dest_port = extract_ip_port(decrypted_data)

    # Create a TCP socket to send the packet to the destination
    dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the destination
    dest_sock.connect((dest_ip, dest_port))

    # Send the packet to the destination
    dest_sock.sendall(decrypted_data)

    # Close the destination socket
    dest_sock.close()

    # Close the tunnel client socket
    tunnel_client.close()
