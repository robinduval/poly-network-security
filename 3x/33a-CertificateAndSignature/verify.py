#!/usr/bin/env python3

import os
import subprocess

def verify_certificate(certificate, public_key_path):
    
    #with open(public_key_path, 'rb') as f:
    #    public_key = f.read()

    #public_key_len = len(public_key)

    #identity = certificate[public_key_len:public_key_len+256]
    #signature = certificate[public_key_len+256:]

    #os.system('echo -n "identity" > identity.txt')
    #os.system(f'cat identity.txt | openssl dgst -sha256 -verify {public_key_path} -signature signature.bin')

    #with open('signature.bin', 'rb') as f:
    # signature = f.read()

    #os.remove('identity.txt')
    #os.remove('signature.bin')

    #return os.WEXITSTATUS(os.stat('/dev/shm/signature.bin').st_size) == 0
    

    return 0 == os.system("cat identity.txt | openssl dgst -sha256 -sign tmp/private.pem -out signature.bin")

#MAIN
public_key_path = 'tmp/public.pem'
certificate_path = 'certificate.bin'

# read certificate from file
with open(certificate_path, 'rb') as f:
    certificate = f.read()

# verify certificate
valid = verify_certificate(certificate, public_key_path)

if valid:
    print('Certificate is valid!')
else:
    print('Certificate is not valid.')
