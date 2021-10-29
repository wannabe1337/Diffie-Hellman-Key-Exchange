# ref. https://crypto.stackexchange.com/questions/3965/what-is-the-main-difference-between-a-key-an-iv-and-a-nonce
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(msg,size):
    while(len(msg)%size!=0):
        msg+=' '
    return msg
def AES_encrypt(message:str,key:bytes):   # 16 bytes of key required
    cipher=AES.new(key,AES.MODE_CBC,IV)
    padded_message=pad(message,AES.block_size)
    cipher_text=cipher.encrypt(padded_message.encode('utf-8'))
    return cipher_text  # bytes type

def AES_decrypt(cipher:str,key:bytes):   # 16 bytes of key required
    decipher=AES.new(key,AES.MODE_CBC,IV)
    decipher_text=decipher.decrypt(cipher)
    message=(decipher_text.decode('utf-8')).rstrip()
    return message  # str type

# key=get_random_bytes(16)
global IV   # Initialization Vector for AES encryption
IV=b'\x0f\xa6\xcb\xdb\x86\nu\x90\xe4\xa0\x91fR)i\xb3'