#!/usr/bin/env python3

import os
import socket
import time
import subprocess
from utils import receive
from utils import send

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