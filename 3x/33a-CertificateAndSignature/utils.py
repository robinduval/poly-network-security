#!/usr/bin/env python3

import os
import socket
import time
import subprocess

def bind_and_listen(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified IP address and port
    s.bind((ip, port))
    
    # Listen for incoming connections
    s.listen()
    print(f"Listening on {ip}:{port}")
    
    # Accept the connection and return the connection object and address
    conn, addr = s.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")
    
    return s, conn

def receive(ip, port, filename):
    # Receive asymmetric public key
    connected = False
    while not connected:
        try:
            s, conn = bind_and_listen(ip, port)
            connected = True
            with conn:
                with open(filename, 'wb') as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
        except ConnectionRefusedError as e:
            # If connection is refused, wait 1 second and try again
            print(f"Connection refused to RECEIVED wait 1 sec {filename} : {e}")
            time.sleep(1)
            continue
            # Ferme la connexion avec le client
        except Exception as e:
            print(f"Error Receiving {filename} : {e}")
            s.close()
            os._exit(1)

def send(ip, port, filename):
    connected = False
    while not connected:
        try:    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                connected = True
                with open(filename, 'rb') as f:
                    data = f.read()
                    s.sendall(data)
        except ConnectionRefusedError as e:
            # If connection is refused, wait 1 second and try again
            print(f"Connection refused to SEND wait 1 sec {filename} : {e}")
            time.sleep(1)
            continue