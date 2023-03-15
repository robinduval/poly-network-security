#!/usr/bin/env python3

import os
import subprocess

def generate_certificate(identity, public_key_path):
    # generate private key
    os.system('openssl genrsa -out private.pem 2048')

    # extract public key
    os.system('openssl rsa -in private.pem -pubout -out public.pem')

    # sign identity
    #identity_bytes = bytes(identity, 'utf-8')
    #os.system(f'echo -n "{identity}" > identity.txt')
    os.system('cat identity.txt | openssl dgst -sha256 -sign private.pem -out signature.bin')

    # create certificate
    with open(public_key_path, 'rb') as f:
        public_key = f.read()

    with open('identity.txt', 'rb') as f:
        identity = f.read()

    with open('signature.bin', 'rb') as f:
        signature = f.read()

    certificate = public_key + identity + signature

    print("prout")
    with open('certificate.bin', 'wb') as f:
        f.write(certificate)

    # cleanup
    os.remove('private.pem')
    os.remove('public.pem')
    os.remove('identity.txt')
    os.remove('signature.bin')

    return certificate

generate_certificate("name:robin", "tmp/public.pem")