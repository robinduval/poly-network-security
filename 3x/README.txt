
# CLIENT // Generate a public key FOR SYMMETRIC CRYPT
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

