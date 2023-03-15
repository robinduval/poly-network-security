#!/usr/bin/env python3

import os
import socket
import subprocess

SERVER_DIR = "server_files/"

CLIENT_DIR = "client_files/"
CLIENT_FILE_RECEIVED_ENCRYPTED = CLIENT_DIR+"encrypted_file.txt"
CLIENT_FILE_RECEIVED_DECRYPTED = CLIENT_DIR+"decrypted_file.txt"

def receive_file(ip, port):
    # Crée une socket pour le serveur et écoute les connexions entrantes
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    # Accepte une connexion entrante
    client_socket, addr = server_socket.accept()

    # Récupère la clé publique envoyée par le client
    client_key = client_socket.recv(1024)

    # Déchiffre la clé symétrique avec la clé privée du serveur
    decrypt_key_process = subprocess.run(["openssl", "rsautl", "-decrypt", "-inkey", "server_key.pem", "-in", CLIENT_DIR+"sym_key.enc", "-out", SERVER_DIR+"sym_key"], stderr=subprocess.PIPE)

    # Check if the decryption process succeeded
    if decrypt_key_process.returncode != 0:
        print(f"An error occurred while decrypting the symmetric key: {decrypt_key_process.stderr.decode('utf-8')}")
        os._exit(1)  # Stop the program

    # Déchiffre le fichier avec la clé symétrique
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-in", CLIENT_FILE_RECEIVED_ENCRYPTED, "-out", CLIENT_FILE_RECEIVED_DECRYPTED, "-k", open(SERVER_DIR+"sym_key", "rb").read()])

    # Ferme la connexion avec le client
    client_socket.close()

    # Ferme la socket du serveur
    server_socket.close()

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
client_ip = '10.0.0.27'
port = 8080
receive_file(client_ip, port)
