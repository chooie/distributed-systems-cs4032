import SocketServer
import socket
import threading

from server_client_package.server.server_core.server_utils import *
from server_client_package.server.server_message.message_handler import \
    message_handler
from server_client_package.shared_lib.constants import MAX_NUMBER_OF_CLIENTS, \
    BUFFER_SIZE, DO_NOT_BLOCK, STUDENT_ID
from server_client_package.shared_lib.error import handle_socket_exception, \
    InformClientError, MessageHandlerError
from server_client_package.server.log import error_processing


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
        handled = False  # Only acquire semaphore on first iteration
        try:
            while True:
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(BUFFER_SIZE)

                if not self.data:
                    break

                # Attempt to acquire semaphore
                if not handled and not semaphore.acquire(DO_NOT_BLOCK):
                    refuse_connection(self)
                    return

                if is_kill_command(self.data):
                    kill_server()

                if begins_with_helo_text(self.data):
                    (host, port) = self.server.server_address
                    handle_helo_message(host, port, STUDENT_ID, self)
                    continue

                # Do work
                message_handler(self)
                handled = True
        except socket.error, e:
            handle_socket_exception(e, self.request)
        except MessageHandlerError, e:
            error_processing(e.original_message)
            self.request.sendall(e.get_error_message())
        except InformClientError, e:
            self.request.sendall(e.get_error_message())
        except TerminateRequestThread:
            pass
        except:
            print "Unexpected error:", sys.exc_info
            raise
        finally:
            print "Client disconnected"
            # Release semaphore on thread destruction
            semaphore.release()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 100
    allow_reuse_address = True
    pass
