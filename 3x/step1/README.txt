#NEW VERSION

# SERVER // ASYMETRIC CRYPT PUBLIC KEY
#           GENERATE PRIVATE
openssl genrsa -out server_private_key_forkey.pem 2048 
#           EXTRACT PUBLIC
openssl rsa -in server_private_key_forkey.pem -pubout -out server_public_key_forkey.pem

# SERVER // SEND PUBLIC KEY (to CLIENT)
connect+sendall

# CLIENT // GENERATE SYMMETRIC KEY
openssl rand -hex 32 > client_key_forfile.txt

# CLIENT // RECEIVE PUBLIC KEY (from SERVER)
DONE

# CLIENT // ENCRYPT SYMMETRIC KEY (WITH PUBLIC SERVER KEY)
openssl enc -aes-256-cbc -salt -in client_key_forfile.txt -out client_key_forfile.enc -pass file:server_public_key_forkey.pem -pbkdf2

# CLIENT // ENCRYPT SYMMETRIC THE DATA
openssl enc -aes-256-cbc -salt -in raw.txt -out raw.enc -pass file:key_forfile.txt -pbkdf2

# CLIENT // SEND ENCRYPTED SYMMETRIC KEY
connect+sendall

# CLIENT // SEND ENCRYPTED DATA
connect+sendall

# SERVER // RECEIVE KEY
bind+listen

# SERVER // RECEIVE DATA
bind+listen

# SERVER // DECRYPT KEY
openssl enc -d -aes-256-cbc -salt -in client_key_forfile.enc -out client_key_forfile.dec -pass file:server_public_key_forkey.pem -pbkdf2

# SERVER // DECRYPT DATA
openssl enc -d -aes-256-cbc -salt -in raw.enc -out raw.dec -pass file:client_key_forfile.dec -pbkdf2

#### OLD VERSION in /tmp/client.py and /tmp/server.py
# CLIENT // Generate# SERVER // ASYMETRIC CRYPT PUBLIC KEY
#           GENERATE PRIVATE
openssl genrsa -out private_key_forkey.pem 2048 
#           EXTRACT PUBLIC
openssl rsa -in private_key_forkey.pem -pubout -out public_key_forkey.pem

# SERVER // SEND PUBLIC KEY (to CLIENT)

# CLIENT // ENCRYPT SERVER PUBLIC  a public key FOR SYMMETRIC CRYPT
openssl rand -hex 32 > key_forfile.txt

# CLIENT // SYMMETRIC CRYPT
openssl enc -aes-256-cbc -salt -in raw.txt -out raw.enc -pass file:key_forfile.txt -pbkdf2

# CLIENT // ASYMETRIC CRYPT PUBLIC KEY
#           GENERATE PRIVATE
openssl genrsa -out private_key_forkey.pem 2048 
#           EXTRACT PUBLIC
openssl rsa -in private_key_forkey.pem -pubout -out public_key_forkey.pem
#           Encrypt the symmetric key with the public asymmetric key
openssl enc -aes-256-cbc -salt -in key_forfile.txt -out key_forfile.enc -pass file:public_key_forkey.pem -pbkdf2

# CLIENT // SEND ASYMETRIC PUBLIC KEY
COMPLETE
# CLIENT // SEND SYMMETRIC CRYPTED FILE
COMPLETE

# CLIENT // SEND ASYMETRIC PUBLIC KEY
COMPLETE
# CLIENT // SEND SYMMETRIC CRYPTED FILE
COMPLETE

# SERVER // DECRYPT ASYMETRIC PUBLIC KEY FROM CLIENT
openssl enc -d -aes-256-cbc -salt -in key_forfile.enc -out key_forfile.txt.dec -pass file:public_key_forkey.pem -pbkdf2

# SERVER // DECRYPT FILE FROM CLIENT WITH DECRYPTED KEY
openssl enc -d -aes-256-cbc -salt -in raw.enc -out raw.dec -pass file:key_forfile.txt -pbkdf2

