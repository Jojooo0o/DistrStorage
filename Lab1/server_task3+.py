from socket import *

max_bytes = 100

def Main():
    s = socket(AF_INET,SOCK_STREAM)

    s.bind(('', 9000))
    s.listen(5)


    while True:
        print('Connecting...')
        (conn, addr) = s.accept()
        print(f'Connected to {addr[0]} : {addr[1]}')
        read_data = True
        string = ''
        while read_data:
            data = conn.recv(max_bytes)
            if repr(data):
                string += data.decode()  
            if not data:
                break
        print(f'Received message: {string} \nfrom: {addr[0]} : {addr[1]}')
        print(f'Closing connection')
        conn.close()

        #start_new_thread(threaded, (conn, addr,))

    #s.close()

if __name__ == '__main__':
    Main()
