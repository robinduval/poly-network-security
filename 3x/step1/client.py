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

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
# MAIN IS HERE // SERVER
client_ip = '10.0.0.26'
server_ip = '10.0.0.27'
serverpubkey_port = 8080
clientsymkey_port = 8081
clientendata_port = 8082
FILE_TO_SEND = "client_files/raw.txt"

receive(client_ip, serverpubkey_port, 'server_public_key_forkey.pem')

print('Generate sym pub key')
with open('client_key_forfile.txt', 'wb') as output_file:
    generate_sym_pub = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=output_file, check=True)
if generate_sym_pub.returncode != 0:
    print(f"An error occurred while generate_sym_pub: {generate_private_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print('Encrypt the file with the Client Key')
encrypt_the_key = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', FILE_TO_SEND, '-out', 'raw.enc', '-pass', 'file:client_key_forfile.txt', '-pbkdf2'], check=True)

print('Encrypt the Client Key with the Server Public Key')
encrypt_the_key = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', 'client_key_forfile.txt', '-out', 'client_key_forfile.enc', '-pass', 'file:server_public_key_forkey.pem', '-pbkdf2'], check=True)

send(server_ip, clientsymkey_port, 'client_key_forfile.enc')
  
send(server_ip, clientendata_port, 'raw.enc')