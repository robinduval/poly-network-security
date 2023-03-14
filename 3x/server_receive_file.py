#!/usr/bin/env python3

import socket

def receive_file(file_path, ip, port):
    # Create a socket and bind it to a specific IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    try:
        # Accept incoming connections and receive file data
        client_socket, client_address = server_socket.accept()
        # print(client_address, "has connected and send file")
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the client socket and server socket
        if client_socket:
            client_socket.close()
        server_socket.close()

filepath = 'received_file.txt'
client_ip = '10.0.0.27'
port = 8080
receive_file(filepath, client_ip, port)