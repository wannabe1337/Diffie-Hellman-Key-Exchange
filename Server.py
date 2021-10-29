import socket
import time
from threading import Thread
import DH_Key_Exchange
# -------------------------------------------------- #

# create a connection oriented IPv4 socket object
serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Server IP and Port address
host='127.0.0.1'
port=20555
# bind the port and ip to socket
try:
    serverSocket.bind((host,port))
    # queue up to 5 request
    serverSocket.listen(5)
    print(f'Listening at {host}:{port} . . .')

except socket.error as e:
    print(str(e))

# -------------------------------------------------- #
# Global Constant and Var
allClients={}
clients=[]
sendr=''
recvr=''
count=0
exchanged=False
# 'a' is primitive root of prime 'n'
a,n=DH_Key_Exchange.dh_key_exchange()

# Different features
def closeClientSock(clientSock):
    clientSock.shutdown(socket.SHUT_RDWR)
    clientSock.close()
    
def keyExchange(sendr,recvr):
    global exchanged
    time.sleep(1)
    sendr.sendall(str.encode(str(a)))
    recvr.sendall(str.encode(str(a)))
    time.sleep(1)
    sendr.sendall(str.encode(str(n)))
    recvr.sendall(str.encode(str(n)))
    time.sleep(1)    
    sendr.send(str.encode('sendr'))
    recvr.send(str.encode('recvr'))
    
    S=sendr.recv(1024) # exchanging original keys
    R=recvr.recv(1024)

    sendr.sendall(R)
    recvr.sendall(S) # exchanging original keys
    time.sleep(1) 
    sendr.send(str.encode("Exchanged"))
    recvr.send(str.encode("Exchanged"))

    exchanged=True


def identify(clientSock):
    global count
    global sendr
    global recvr
    global clients
    # Identifying User
    username=clientSock.recv(2048).decode('utf-8')
    allClients[username]=clientSock
    clients.append(clientSock)
    if(count==0):
        sendr=username
    else:
        recvr=username
    count+=1
    return username


# -------------------------------------------------- #
def thread_client(clientSock):
    global count
    global sendr
    global recvr
    global exchanged
    global clients
    username=identify(clientSock)
    clientSock.send(str.encode(f"Hey {username} !\nType 'Exit' to terminate connection.\nWaiting for Receiver . . ."))

# Waiting for receiver
    while(count!=2):
        pass

# Sends ready signal
    time.sleep(0.5)
    clientSock.send(str.encode("ready"))
    if(allClients[sendr]==clientSock):
        keyExchange(allClients[sendr],allClients[recvr])
    
# Wait for key exchange
    while(not exchanged):
        pass

# Start Chatting
    while(True):
        data=(clientSock.recv(2048))
        try:
            if((data.decode('utf-8')).lower()=='exit'):
                for client in clients :
                    client.sendall(str.encode('exit'))  
                    client.close()  
                return
        except:
            # Send msg to all except the sender
            for client in clients :
                if (client!=clientSock):
                    client.sendall(data)
# -------------------------------------------------- #
# establish a connection to a client
while(True):
    clientSocket,addr=serverSocket.accept()
    print(f'Connected to {addr[0]}:{addr[1]}')
    # --------------------------------------------- #
    t=Thread(None,target=thread_client,args=(clientSocket,))
    t.start()
# --------------------------------------------- #