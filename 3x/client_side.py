#!/usr/bin/env python3

import os
import socket
import subprocess

# Chemin d'accès aux fichiers du serveur et du client
SERVER_DIR = "server_files/"

CLIENT_DIR = "client_files/"
CLIENT_FILE_TO_SEND = CLIENT_DIR+"raw.txt"
CLIENT_FILE_TO_SEND_ENCRYPTED = CLIENT_DIR+"encrypted_file.txt"


def send_file(ip, port):
	# Connecte le client au serveur
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ip, port))

	# Récupère la clé publique du serveur
	subprocess.run(["openssl", "rsa", "-in", f"{SERVER_DIR}server_key.pem", "-pubout", "-out", f"{CLIENT_DIR}server_key.pub"])

	# Génère une clé symétrique aléatoire
	sym_key = os.urandom(32)

	# Chiffre la clé symétrique avec la clé publique du serveur
	subprocess.run(["openssl", "rsautl", "-encrypt", "-inkey", f"{CLIENT_DIR}server_key.pub", "-pubin", "-in", f"{CLIENT_DIR}sym_key", "-out", f"{CLIENT_DIR}sym_key.enc"])

	# Envoie la clé symétrique chiffrée au serveur
	sym_key_enc = open(f"{CLIENT_DIR}sym_key.enc", "rb").read()
	client_socket.sendall(sym_key_enc)

	# Chiffre le fichier avec la clé symétrique
	subprocess.run(["openssl", "enc", "-aes-256-cbc", "-in", f"{CLIENT_FILE_TO_SEND}", "-out", f"{CLIENT_FILE_TO_SEND_ENCRYPTED}", "-k", f"{sym_key}"])

	# Envoie le fichier chiffré au serveur
	encrypted_file = open(f"{CLIENT_FILE_TO_SEND_ENCRYPTED}", "rb").read()
	client_socket.sendall(encrypted_file)

	# Ferme la connexion avec le serveur
	client_socket.close()

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
server_ip = '10.0.0.27'
port = 8080
send_file(server_ip, port)
