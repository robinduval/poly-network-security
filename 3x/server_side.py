#!/usr/bin/env python3


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

	# Récupère la clé privée du serveur
	subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", f"{SERVER_DIR}server_key.pem"])

	# Récupère la clé publique envoyée par le client
	client_key = client_socket.recv(1024)

	# Déchiffre la clé symétrique avec la clé privée du serveur
	subprocess.run(["openssl", "rsautl", "-decrypt", "-inkey", f"{SERVER_DIR}server_key.pem", "-in", f"{CLIENT_DIR}sym_key.enc", "-out", f"{SERVER_DIR}sym_key"])

	# Déchiffre le fichier avec la clé symétrique
	subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-in", f"{CLIENT_FILE_RECEIVED_ENCRYPTED}", "-out", f"{CLIENT_FILE_RECEIVED_DECRYPTED}", "-k", open(f"{SERVER_DIR}sym_key", "rb").read()])

	# Ferme la connexion avec le client
	client_socket.close()

	# Ferme la socket du serveur
	server_socket.close()

# SERVER : Parrot   : 10.0.0.27
# CLIENT : RUNBUNTU : 10.0.0.26
client_ip = '10.0.0.27'
port = 8080
receive_file(client_ip, port)