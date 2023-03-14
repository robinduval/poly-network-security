#!/usr/bin/env python3

import socket

def receive_file(file_path, ip, port):
    # Create a socket and bind it to a specific IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    # Accept incoming connections and receive file data
    client_socket, address = server_socket.accept()
    with open(file_path, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data+data)

    # Close the client socket and server socket
    client_socket.close()
    server_socket.close()

filepath = 'received_file.txt'
client_ip = '10.0.0.27'
port = 8080
receive_file(filepath, client_ip, port)