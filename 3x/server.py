#!/usr/bin/env python3

import os
import socket
import time
import subprocess

# Chemin d'accès aux fichiers du serveur et du client
SERVER_DIR = "server_files/"
CLIENT_DIR = "client_files/"

import socket
import subprocess

def receive(ip, key_port, file_port):
    # RECEIVE ASYMETRIC PUBLIC KEY
    connected = False
    while not connected:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((ip, key_port))
                s.listen()
                print('Listen Key')
                conn, addr = s.accept()
                connected = True
                with conn:
                    with open('public_key_forkey.pem', 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
        except ConnectionRefusedError:
            # If connection is refused, wait 1 second and try again
            time.sleep(1)
            continue
    # Ferme la connexion avec le client
    s.close()
    

    # RECEIVE SYMMETRIC CRYPTED FILE
    connected = False
    while not connected:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((ip, file_port))
                s.listen()
                print('Listen File')
                conn, addr = s.accept()
                connected = True
                with conn:
                    with open('raw.enc', 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
        except ConnectionRefusedError:
            # If connection is refused, wait 1 second and try again
            time.sleep(1)
            continue

    # Ferme la connexion avec le client
    s.close()
    
    # DECRYPT ASYMETRIC PUBLIC KEY FROM CLIENT
    subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'key_forfile.enc', '-out', 'key_forfile.txt.dec', '-pass', 'file:public_key_forkey.pem', '-pbkdf2'], check=True)
    
    # DECRYPT FILE FROM CLIENT WITH DECRYPTED KEY
    subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'raw.enc', '-out', 'raw.dec', '-pass', 'file:key_forfile.txt', '-pbkdf2'], check=True)

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
client_ip = '10.0.0.27'
key_port = 8080
file_port = 8081
receive(client_ip, key_port,file_port)
