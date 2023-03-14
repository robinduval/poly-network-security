#!/usr/bin/env python3

import socket

def send_file(file_path, ip, port):
    # Create a socket and connect to the remote server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    # Open the file to be sent and read its contents
    with open(file_path, 'rb') as file:
        file_contents = file.read()

    # Send the file contents to the server in chunks
    client_socket.sendall(file_contents)

    # Close the socket
    client_socket.close()

filepath = 'raw.txt'
server_ip = '10.0.0.27'
port = 8080
send_file('raw.txt', server_ip, port)