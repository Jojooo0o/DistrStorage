from socket import *
import keyboard
import os

MAX_BYTES = 4096

def selectMode():
    modus = int(input('Insert 1 (String mode) or 2 (Random byte mode)'))
    return modus

def customInput():
    string = input('Insert custom string to send: ')
    if len(string) > MAX_BYTES:
        string = string[:MAX_BYTES]
    return str.encode(string)

def randomBytes():
    rand_len = int(input('Define number of bytes: '))
    string = os.urandom(rand_len)
    return str.encode(string) 



def Main():
    s = socket(AF_INET, SOCK_STREAM)
    
    while True:
        s.connect(('localhost', 9000))
        modus = 0
        while modus != 1 or modus != 2:
            modus = selectMode()
        if modus == 1:
            data = customInput()
        elif modus == 2:
            data = randomBytes()
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