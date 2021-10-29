import random
import socket
from threading import Thread
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import CryptoAES
import CryptoHKDF

# Constant and variable
exchanged=False

# create clientSocket object
clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server's IP and Port address
host='127.0.0.1'
port=20555

# Connect to server
try:
    clientSocket.connect((host,port))
except socket.error as e:
    print(str(e))
# ----------------------------------------------
# Constant and variables
key=0

# Different Features
def recvrExchangeKey(a,n):
    q=random.randint(20,30)
    R=(a**q) % n
    clientSocket.sendall(str.encode(str(R)))
    S=int((clientSocket.recv(1024)).decode('utf-8'))
    key=(S**q) % n
    return key
def sendrExchangeKey(a,n):
    p=random.randint(20,30)
    S=(a**p) % n
    clientSocket.sendall(str.encode(str(S)))
    R=int((clientSocket.recv(1024)).decode('utf-8'))
    key=(R**p) % n
    return key

def keyExchange():
    print("Exchanging Keys . . .")
    a=int((clientSocket.recv(1024)).decode('utf-8'))
    n=int((clientSocket.recv(1024)).decode('utf-8'))

    sendr_recvr=(clientSocket.recv(1024)).decode('utf-8')
    if(sendr_recvr=="sendr"):
        return sendrExchangeKey(a,n)
    else:
        return recvrExchangeKey(a,n)

# Chit-Chat
def recv_message():
    print(">>>>>>> Welcome to the chat box <<<<<<<")
    while(True):
        try:
            Reply=clientSocket.recv(1024)
            if(Reply):
                try:
                    if (Reply.decode('utf-8')=='exit'): # if server closes connection
                        print('Disconnected !')
                        return
                except:
                    message=CryptoAES.AES_decrypt(Reply,secret)
                    print(message)
        except socket.error as e:
            print(e)
            return

t=Thread(None,target=recv_message) # thread that keep listening for messages

# -------------------------------------------------------
user=input('Enter Username: ')
clientSocket.send(str.encode(user))    # identifying users
print((clientSocket.recv(1024)).decode('utf-8'))    # Welcome Msg
print(clientSocket.recv(1024).decode('utf-8'))      # if both clients are ready

print('key = ',keyExchange())    # print exchanged keys

# Waiting for key exchange
msgr=(clientSocket.recv(1024)).decode('utf-8')
print("Exchanged Keys Successfully !")

# Key [Secret key for encryption/decryption] Derivation from exchanged key
secret=CryptoHKDF.hkdf(16,str(key).encode('utf-8'),b"salt")  # ikm(input keying material)=key 
print("Key For Enc/Dec = ",secret)

# Start chatting
t.start()
while(True):    # Waits for user messages
    if(t.is_alive()):
        try:
            message=input('')
            if(message.lower()!=exit):
                message=user+':'+message
                cipher=CryptoAES.AES_encrypt(message,secret)
                clientSocket.send(cipher)
            else:
                clientSocket.send(str.encode(message))
        except: # if clients terminates during chat
            try:
                clientSocket.send(str.encode("EXIT"))
            except socket.error as e:
                clientSocket.close()


    else:
        clientSocket.close()
        exit()

# ----------------------------------------------