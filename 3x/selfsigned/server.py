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
clientsignat_port = 8083

print("Generate Private Key")
generate_private_key = subprocess.run(['openssl', 'genrsa', '-out', 'private.pem', '2048'], check=True)
if generate_private_key.returncode != 0:
    print(f"An error occurred while generate_private_key: {generate_private_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print("Extract Public Key")
extract_public_key = subprocess.run(['openssl', 'rsa', '-in', 'private.pem', '-pubout', '-out', 'public.pem'], check=True)
if extract_public_key.returncode != 0:
    print(f"An error occurred while extract_public_key: {extract_public_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program
  
send(client_ip, serverpubkey_port, 'public.pem')

receive(server_ip, clientsymkey_port, 'client_key.enc')

receive(server_ip, clientendata_port, 'raw.enc')

receive(server_ip, clientsignat_port, 'signature.bin')

print("Decrypt Client Key")
decrypt_client_key = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'client_key.enc', '-out', 'client_key.dec', '-pass', 'file:public.pem', '-pbkdf2'], check=True)
if decrypt_client_key.returncode != 0:
    print(f"An error occurred while decrypt_client_key: {decrypt_client_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print("Decrypt Data")
decrypt_data = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-salt', '-in', 'raw.enc', '-out', 'raw.dec', '-pass', 'file:client_key.dec', '-pbkdf2'], check=True)
if decrypt_data.returncode != 0:
    print(f"An error occurred while decrypt_data: {decrypt_data.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print("Is the file correct ?") 

# read raw data from file
with open('raw.dec', 'rb') as f:
    raw_data = f.read()

# run openssl command to verify signature
openssl_command = ['openssl', 'dgst', '-sha256', '-verify', 'public.pem', '-signature', 'signature.bin']

try:
    subprocess.run(openssl_command, input=raw_data, check=True)
    print('Signature is valid!')
except subprocess.CalledProcessError:
    print('Signature is not valid.')
