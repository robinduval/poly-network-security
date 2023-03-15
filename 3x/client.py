#!/usr/bin/env python3

import os
import socket
import subprocess

# Chemin d'accès aux fichiers du serveur et du client
SERVER_DIR = "server_files/"
CLIENT_DIR = "client_files/"
FILE_TO_SEND = "client_files/raw.txt"

def send(ip, port):
    # Generate a public key FOR SYMMETRIC CRYPT
    print('Generate sym pub key')
    with open('key_forfile.txt', 'wb') as output_file:
        subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=output_file, check=True)

    # SYMMETRIC CRYPT
    print('Encrypt the file')
    subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', FILE_TO_SEND, '-out', 'raw.enc', '-pass', 'file:key_forfile.txt', '-pbkdf2'], check=True)
    
    # ASYMMETRIC CRYPT PUBLIC KEY
    
    ## GENERATE PRIVATE
    print('Generate asym priv key')
    subprocess.run(['openssl', 'genrsa', '-out', 'private_key_forkey.pem', '2048'], check=True)
    
    ## EXTRACT PUBLIC
    print('Extract asym pub key')
    subprocess.run(['openssl', 'rsa', '-in', 'private_key_forkey.pem', '-pubout', '-out', 'public_key_forkey.pem'], check=True)
    
    ## Encrypt the symmetric key with the public asymmetric key
    print('Encrypt key')
    subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', 'key_forfile.txt', '-out', 'key_forfile.enc', '-pass', 'file:public_key_forkey.pem', '-pbkdf2'], check=True)
    
    # SEND ASYMETRIC PUBLIC KEY
    print('SEND ASYM KEY')
    connected = False
    while not connected:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, key_port))
                connected = True
                with open('public_key_forkey.pem', 'rb') as f:
                    data = f.read()
                    s.sendall(data)
        except ConnectionRefusedError:
            # If connection is refused, wait 1 second and try again
            time.sleep(1)
            continue
            
    # SEND SYMMETRIC CRYPTED FILE
    print('SEND CRYPTED FILE')
    connected = False
    while not connected:
        try:    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, file_port))
                connected = True
                with open('raw.enc', 'rb') as f:
                    data = f.read()
                    s.sendall(data)
        except ConnectionRefusedError:
            # If connection is refused, wait 1 second and try again
            time.sleep(1)
            continue

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
key_port = 8080
file_port = 8081
send(client_ip, key_port, file_port)
