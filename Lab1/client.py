from socket import *
import keyboard
import os
import sys

MAX_BYTES = 4096

def selectMode():
    modus = int(input('Insert 1 (String mode) or 2 (Random byte mode):'))
    print(modus)
    if modus == 1 or modus == 2:
        return modus
    else:
        modus = selectMode()

def customInput():
    string = input('Insert custom string to send: ')
    if len(string) > MAX_BYTES:
        string = string[:MAX_BYTES]
    return str.encode(string)

def randomBytes():
    byte_obj = bytes()
    rand_len = int(input('Define number of bytes: '))
    if(rand_len >= 4294967296):
        print('Please choose a number smaller than 4294967295')
        return randomBytes()
    print(rand_len.to_bytes(length=4, byteorder=sys.byteorder))
    byte_obj += rand_len.to_bytes(length=4, byteorder=sys.byteorder)
    return os.urandom(rand_len)
    #return str.encode(string) 



def Main():
    s = socket(AF_INET, SOCK_STREAM)
    
    while True:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 9000))
        modus = selectMode()
        if modus == 1:
            data = customInput()
        elif modus == 2:
            data = randomBytes()
        s.send(modus.to_bytes(length=1, byteorder=sys.byteorder))
        s.send(data)

        s.close()
        

if __name__ == '__main__':
    Main()


# print('Insert string:')
usr_in = input('Insert custom String: ')

# IS ONE BYTE ONE CHAR?
usr_in_byte_len = len(usr_in.encode('utf-8'))
print(f'{str(usr_in_byte_len)}')
#print(f'You have inserted: "{usr_in}"')
#print(len(str.encode(usr_in)))
#print(type(str.encode(usr_in)))

if(len(usr_in) > MAX_BYTES):
    usr_in = usr_in[:MAX_BYTES]

s.send(str.encode(usr_in))
#data = s.recv(10000)
#print(data)
s.close()