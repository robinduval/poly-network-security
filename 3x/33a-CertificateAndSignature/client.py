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
clientsigkey_port = 8082
clientendata_port = 8083
clientsignat_port = 8084

receive(client_ip, serverpubkey_port, 'public.pem')

print("Generate Private Key")
generate_private_key = subprocess.run(['openssl', 'genrsa', '-out', 'client_private.pem', '2048'], check=True)
if generate_private_key.returncode != 0:
    print(f"An error occurred while generate_private_key: {generate_private_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print("Extract Public Key")
extract_public_key = subprocess.run(['openssl', 'rsa', '-in', 'client_private.pem', '-pubout', '-out', 'client_public.pem'], check=True)
if extract_public_key.returncode != 0:
    print(f"An error occurred while extract_public_key: {extract_public_key.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print('Generate Client Key')
with open('client_key.txt', 'wb') as output_file:
    generate_sym_pub = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=output_file, check=True)
if generate_sym_pub.returncode != 0:
    print(f"An error occurred while generate_sym_pub: {generate_sym_pub.stderr.decode('utf-8')}")
    os._exit(1)  # Stop the program

print('Sign the file')
# read raw data from file
with open('raw.txt', 'rb') as f:
    raw_data = f.read()
openssl_command = ['openssl', 'dgst', '-sha256', '-sign', 'client_private.pem', '-out', 'signature.bin']
try:
    subprocess.run(openssl_command, input=raw_data, check=True)
    print('Signature has been done!')
except subprocess.CalledProcessError:
    print('Signature has failed.')

print('Encrypt the file with the Client Key')
encrypt_the_key = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', 'raw.txt', '-out', 'raw.enc', '-pass', 'file:client_key.txt', '-pbkdf2'], check=True)

print('Encrypt the Client Key with the Server Public Key')
encrypt_the_key = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-salt', '-in', 'client_key.txt', '-out', 'client_key.enc', '-pass', 'file:public.pem', '-pbkdf2'], check=True)

send(server_ip, clientsymkey_port, 'client_key.enc')
  
send(server_ip, clientendata_port, 'raw.enc')
  
send(server_ip, clientsignat_port, 'signature.bin')

send(server_ip, clientsigkey_port, 'client_public.pem')