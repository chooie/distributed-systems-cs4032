import sys
import SocketServer
import socket
import threading


from server_client_package.server.server_core.server_utils import \
    begins_with_helo_text, handle_helo_message, is_kill_command, kill_server, \
    refuse_connection, TerminateRequestThread
from server_client_package.server.server_message.message_handler import \
    message_handler
from server_client_package.shared_lib.constants import MAX_NUMBER_OF_CLIENTS, \
    BUFFER_SIZE, DO_NOT_BLOCK, STUDENT_ID
from server_client_package.shared_lib.error import handle_socket_exception, \
    InformClientError, MessageHandlerError
from server_client_package.server.log import error_processing, processing
from server_client_package.server.chat.chat import Chat


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # If semaphore blocks, client's connection will be refused
    semaphore = threading.BoundedSemaphore(MAX_NUMBER_OF_CLIENTS)
    chat = Chat()

    def __init__(self, client_address, request, server):
        # Not set until it is read from client
        self.data = None
        self.chat = ThreadedTCPRequestHandler.chat
        self.terminate_request = False
        SocketServer.BaseRequestHandler.\
            __init__(self, client_address, request, server)

    def handle(self):
        semaphore = ThreadedTCPRequestHandler.semaphore
        handled = False  # Only acquire semaphore on first iteration

        try:
            while True:
                if self.terminate_request:
                    raise TerminateRequestThread

                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(BUFFER_SIZE)

                processing(self.data)

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
                try:
                    message_handler(self)
                    handled = True
                except MessageHandlerError, e:
                    error_processing(e.original_message)
                    self.request.sendall(e.get_error_message())
                except InformClientError, e:
                    sys.stdout.write("Informing client of error\n")
                    self.request.sendall(e.get_error_message())
                except:
                    raise
        except socket.error, e:
            handle_socket_exception(e, self.request)
        except TerminateRequestThread:
            sys.stdout.write("Terminate thread\n")
            pass
        except:
            print "Unexpected error:", sys.exc_info
            kill_server()
        finally:
            sys.stdout.write("Client disconnected\n")
            # Release semaphore on thread destruction
            if handled:
                semaphore.release()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 100
    allow_reuse_address = True
    pass
