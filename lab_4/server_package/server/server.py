import SocketServer
import threading

import log
import server_utils as utils
from server_worker import server_worker

BUFFER_SIZE = 1024
HOST = "0.0.0.0"
PORT = 8080
MAX_NUMBER_OF_CLIENTS = 10
DO_NOT_BLOCK = False

# If semaphore blocks, client's connection will be refused
semaphore = threading.BoundedSemaphore(MAX_NUMBER_OF_CLIENTS)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, client_address, request, server):
        # Not set until it is read from client
        self.data = None
        SocketServer.BaseRequestHandler.\
            __init__(self, client_address, request, server)

    def handle(self):

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(BUFFER_SIZE)

        log.processing(self.data)

        if utils.is_kill_command(self.data):
            utils.kill_server()

        # Attempt to acquire semaphore
        if not semaphore.acquire(DO_NOT_BLOCK):
            utils.refuse_connection(self)
            return

        # Do work
        server_worker(HOST, PORT, self, semaphore)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 100
    allow_reuse_address = True
    pass


def run():
    server = None

    try:
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        log.server_start(server_thread)

        while True:
            # Loop until server shut down
            pass
    except (KeyboardInterrupt, SystemExit):
        utils.clean_up_server(server)

if __name__ == "__main__":
    run()