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
    with open('key_forfile.txt', 'wb') as output_file:
        subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=output_file, check=True)

    # SYMMETRIC CRYPT
    subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', FILE_TO_SEND, '-out', 'raw.enc', '-pass', 'file:key_forfile.txt', '-pbkdf2'], check=True)
    
    # ASYMMETRIC CRYPT PUBLIC KEY
    # GENERATE PRIVATE
    subprocess.run(['openssl', 'genrsa', '-out', 'private_key_forkey.pem', '2048'], check=True)
    # EXTRACT PUBLIC
    subprocess.run(['openssl', 'rsa', '-in', 'private_key_forkey.pem', '-pubout', '-out', 'public_key_forkey.pem'], check=True)
    # Encrypt the symmetric key with the public asymmetric key
    subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', 'key_forfile.txt', '-out', 'key_forfile.enc', '-pass', 'file:public_key_forkey.pem', '-pbkdf2'], check=True)
    
    # SEND ASYMETRIC PUBLIC KEY
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        with open('public_key_forkey.pem', 'rb') as f:
            data = f.read()
            s.sendall(data)
    
    # SEND SYMMETRIC CRYPTED FILE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        with open('raw.enc', 'rb') as f:
            data = f.read()
            s.sendall(data)

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
server_ip = '10.0.0.27'
port = 8080
send(server_ip, port)
