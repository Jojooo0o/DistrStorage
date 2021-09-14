import gevent
import gevent.pywsgi
import gevent.queue

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

import base64
import random, string

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 80), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)

@dispatcher.public
def reverse_string(s):
    return s[::-1]

@dispatcher.public
def store_file(filename, data):
    binary_data = base64.b64decode(data)
    base64_string = base64.b64encode(binary_data)
    if not filename:
        filename_len = 8
        filename = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits) for n in range(filename_len)])
        filename += '.bin'
    try:
        file = open('./'+filename, 'wb')
        file.close()
        with open('./'+filename, 'r+b') as f:
            f.write(base64_string)
    except EnvironmentError as e:
        print(f'Error writing file: {e}')
        return None
    return filename


# in the main greenlet, run our rpc_server
rpc_server.serve_forever()