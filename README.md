# Diffie-Hellman-Key-Exchange
Implemented Diffie-Hellman key exchange from scratch and demonstrated secure communication using client-server one-to-one text based chat program.

**DH_Key_Exchange.py** : It generates a prime number 'n' and primitive-root 'a' of 'n'. These numbers will be used in exchanging the keys.

**Client.py** and **Server.py** : Client and Server for text based chat app. (Only works with two client, and _key exchanges_ when both clients comes online.)

**CryptoHKDF.py** : The key exchanged between clients are basically a integer number. But to demonstrate the secure communication between clients using _**Rijndael Cipher**_(AES), we need 128-bit key. Therefore, we'll use this **_HMAC-based Key Derivation Function_** to derive 128-bit SecretKey.

**CryptoAES.py** : It will take care of all the encryption/decryption of messages between clients. Here, I've used CBC(Cipher Block Chaining) mode to encrypt and decrypt. And as this CBC mode requires IV(Initialization Vector 128-bit), I defined it as constant. 

**Required Library files**
pycryptodome (For AES)
tqdm  (For Showing Progress Bar)
socket
math
threading
random
time
hmac
hashlib

**How to test**
First run the _server_ then run two instances of _client_ representing two different users, then wait for key exchange. Once key got exchanged both the client can start chatting with each other.
