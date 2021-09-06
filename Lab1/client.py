from socket import *
import keyboard
import os
import sys

MAX_BYTES = 4096

def selectMode():
    modus = int(input('Insert 1 (String mode) or 2 (Random byte mode):'))
    print(modus)
    if modus == 1 or modus == 2 or modus == 3:
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
    byte_obj += os.urandom(rand_len)
    return byte_obj
    #return str.encode(string) 



def readFile():
    filename = input('Define file name: ')
    try:
        with open('./'+filename, 'rb') as f:
            data = f.read()
            print(type(data))
            return filename, data
    except EnvironmentError as e:
        print(f'Error reading file: {e}')
        return None
    

def Main():
    s = socket(AF_INET, SOCK_STREAM)
    
    while True:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 9000))
        modus = selectMode()
        filename = ''
        data = bytes()
        if modus == 1:
            data = customInput()
        elif modus == 2:
            data = randomBytes()
        elif modus == 3:
            filename, data = readFile()
        s.send(modus.to_bytes(length=1, byteorder=sys.byteorder))
        if modus == 3:
            print(f'what:({filename})')
            s.send(str.encode(filename))
            feedback = s.recv(2)
            print(repr(feedback))
        #print(len(data))
        s.send(data)

        s.close()
        

if __name__ == '__main__':
    Main()