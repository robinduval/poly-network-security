import socket
import subprocess

# Chemin d'accès aux fichiers du serveur et du client PROUT
SERVER_DIR = "server_files/"
CLIENT_DIR = "client_files/"

# Crée une socket pour le serveur et écoute les connexions entrantes
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
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
subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-in", f"{CLIENT_DIR}encrypted_file", "-out", f"{SERVER_DIR}decrypted_file", "-k", open(f"{SERVER_DIR}sym_key", "rb").read()])

# Ferme la connexion avec le client
client_socket.close()

# Ferme la socket du serveur
server_socket.close()