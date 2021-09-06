from socket import *
import sys
import random, string

MAX_BYTES = 4096

def readString(conn, addr):
    string = ''
    while True:
        data = conn.recv(MAX_BYTES)
        if repr(data):
            string += data.decode()
            if '.pdf' in string:
                break
        if not data:
            break
    
    print(f'Received message: ({string}) \nfrom: {addr[0]} : {addr[1]}')
    print(f'Closing connection')
    return string

def readBinary(conn, addr):
    byte_obj = bytes()
    byte_len = conn.recv(4)
    msg_len = int.from_bytes(byte_len, byteorder=sys.byteorder)

    print(f'byte string length: {msg_len}')

    while True:
        data = conn.recv(MAX_BYTES)
        if repr(data):
            byte_obj += data
        if not data:
            break
    writeFile(byte_obj)


def writeFile(data, filename=None):
    if not filename:
        filename_len = 8
        filename = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for n in range(filename_len)])
        filename += '.bin'
    try:
        file = open('./'+filename, 'wb')
        file.close()
        with open('./'+filename, 'r+b') as f:
            f.write(data)
    except EnvironmentError as e:
        print(f'Error writing file: {e}')
        return None
    return filename


def copyFile(conn, addr):
    filename = readString(conn, addr)
    byte_obj = bytes()
    conn.send(str.encode('OK'))
    while True:
        data = conn.recv(MAX_BYTES)
        if repr(data):
            byte_obj += data
        if not data:
            break
    writeFile(byte_obj, 'copy_'+filename)


def Main():
    s = socket(AF_INET,SOCK_STREAM)

    s.bind(('', 9000))
    s.listen(5)


    while True:
        print('Connecting...')
        (conn, addr) = s.accept()
        print(f'Connected to {addr[0]} : {addr[1]}')
        msg_type_byte = conn.recv(1)
        msg_type = int.from_bytes(msg_type_byte, byteorder=sys.byteorder)
        print(f'MSG TYPE: {msg_type}')
        if msg_type == 1:
            readString(conn, addr)
        elif msg_type == 2:
            readBinary(conn, addr)
        elif msg_type == 3:
            copyFile(conn, addr)
        conn.close()

        #start_new_thread(threaded, (conn, addr,))

    #s.close()

if __name__ == '__main__':
    Main()
