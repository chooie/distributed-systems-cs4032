import SocketServer
import threading
import sys
import log
import socket
import server_utils as utils
from message_handler import message_handler
from ..shared_lib.error import handle_socket_exception

BUFFER_SIZE = 1024
HOST = "0.0.0.0"
PORT = 8080
MAX_NUMBER_OF_CLIENTS = 10
DO_NOT_BLOCK = False


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # If semaphore blocks, client's connection will be refused
    semaphore = threading.BoundedSemaphore(MAX_NUMBER_OF_CLIENTS)

    def __init__(self, client_address, request, server):
        # Not set until it is read from client
        self.data = None
        SocketServer.BaseRequestHandler.\
            __init__(self, client_address, request, server)

    def handle(self):
        semaphore = ThreadedTCPRequestHandler.semaphore
        handled = False
        try:
            while True:
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(BUFFER_SIZE)

                if not self.data:
                    break

                # Attempt to acquire semaphore
                if not handled and not semaphore.acquire(DO_NOT_BLOCK):
                    utils.refuse_connection(self)
                    return

                if utils.is_kill_command(self.data):
                    utils.kill_server()

                # Do work
                message_handler(HOST, PORT, self)
                handled = True
        except socket.error, e:
            handle_socket_exception(e, self.request)
        except:
            print "Unexpected error:", sys.exc_info()[0]
        finally:
            # TODO Release semaphore on thread destruction
            # Release semaphore
            semaphore.release()


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
