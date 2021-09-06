from socket import *
from _thread import *
import threading

print_lock = threading.Lock()

def threaded(connection, address):
    print(f'{address} connected')
    with connection as c:
        while True:
            data = c.recv(1024)
            if repr(data):
                print(f'Detected: {repr(data)}')
            if not data:
                print_lock.release()
                break
        c.close()


def Main():
    s = socket(AF_INET,SOCK_STREAM)

    s.bind(('', 9000))
    s.listen(5)


    while True:
        (conn, addr) = s.accept()

        print_lock.acquire()
        print(f'Connected to: {addr[0]} : {addr[1]}')  

        start_new_thread(threaded, (conn, addr,))

    s.close()

if __name__ == '__main__':
    Main()


"""

    print(f'Received connection from {addr}')
        
    with conn:
        print(f'{addr} connected')
        while True:
            data = conn.recv(1024)
            if repr(data):
                print(f'Detected: {repr(data)}')
            if not data:
                break
except:
    print(f'connection lost to')
    s.close()
*/
"""