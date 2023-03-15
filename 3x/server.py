#!/usr/bin/env python3

import os
import socket
import subprocess

# Chemin d'accès aux fichiers du serveur et du client
SERVER_DIR = "server_files/"
CLIENT_DIR = "client_files/"

import socket
import subprocess

def receive(ip, port):
    # RECEIVE ASYMETRIC PUBLIC KEY
    print('RECEIVE CRYPTED KEY')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            with open('public_key_forkey.pem', 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
    
    # RECEIVE SYMMETRIC CRYPTED FILE
    print('RECEIVE CRYPTED FILE')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            with open('raw.enc', 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
    
    # DECRYPT ASYMETRIC PUBLIC KEY FROM CLIENT
    subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'key_forfile.enc', '-out', 'key_forfile.txt.dec', '-pass', 'file:public_key_forkey.pem', '-pbkdf2'], check=True)
    
    # DECRYPT FILE FROM CLIENT WITH DECRYPTED KEY
    subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'raw.enc', '-out', 'raw.dec', '-pass', 'file:key_forfile.txt', '-pbkdf2'], check=True)
    
    # Ferme la connexion avec le client
    client_socket.close()

    # Ferme la socket du serveur
    server_socket.close()

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
client_ip = '10.0.0.27'
port = 8080
receive(client_ip, port)