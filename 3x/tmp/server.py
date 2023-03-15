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

def receive(ip, key_port, asym_key_port, file_port):
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
    
    # RECEIVE KEY FOR FILE
    connected = False
    while not connected:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((ip, asym_key_port))
                s.listen()
                print('Listen Key For File')
                conn, addr = s.accept()
                connected = True
                with conn:
                    with open('key_forfile.enc', 'wb') as f:
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
    # openssl enc -d -aes-256-cbc -salt -in key_forfile.enc -out key_forfile.txt.dec -pass file:public_key_forkey.pem -pbkdf2
    decrypt_key_process = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'key_forfile.enc', '-out', 'key_forfile.txt.dec', '-pass', 'file:public_key_forkey.pem', '-pbkdf2'], check=True)
    if decrypt_key_process.returncode != 0:
        print(f"An error occurred while decrypting the symmetric key: {decrypt_key_process.stderr.decode('utf-8')}")
        os._exit(1)  # Stop the program

    # DECRYPT FILE FROM CLIENT WITH DECRYPTED KEY
    # openssl enc -d -aes-256-cbc -salt -in raw.enc -out raw.dec -pass file:key_forfile.txt -pbkdf2
    decrypt_file_process = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'raw.enc', '-out', 'raw.dec', '-pass', 'file:key_forfile.txt.dec', '-pbkdf2'], check=True)
    
    if decrypt_file_process.returncode != 0:
        print(f"An error occurred while decrypting the symmetric key: {decrypt_file_process.stderr.decode('utf-8')}")
        os._exit(1)  # Stop the program


# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
ip = '10.0.0.27'
key_port = 8080
asym_key_port = 8081
file_port = 8082
receive(ip, key_port, asym_key_port, file_port)