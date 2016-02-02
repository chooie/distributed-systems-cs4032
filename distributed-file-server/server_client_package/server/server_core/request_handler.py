import sys
import SocketServer
import socket
import threading

from server_utils import begins_with_helo_text, handle_helo_message, \
    is_kill_command, kill_server, refuse_connection, TerminateRequestThread
from shared_lib.constants import MAX_NUMBER_OF_CLIENTS, BUFFER_SIZE, \
    DO_NOT_BLOCK, STUDENT_ID
from shared_lib.error import handle_socket_exception
from server.log import processing


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # If semaphore blocks, client's connection will be refused
    semaphore = threading.BoundedSemaphore(MAX_NUMBER_OF_CLIENTS)
    handler_num = 0

    def __init__(self, client_address, request, server):
        # Not set until it is read from client
        self.data = None
        self.terminate_request = False
        SocketServer.BaseRequestHandler.\
            __init__(self, client_address, request, server)

    def handle_message(self):
        print "You shouldn't see this."

    def handle(self):
        semaphore = ThreadedTCPRequestHandler.semaphore
        handled = False  # Only acquire semaphore on first iteration

        my_num = ThreadedTCPRequestHandler.handler_num
        ThreadedTCPRequestHandler.handler_num += 1

        try:
            while True:
                if self.terminate_request:
                    raise TerminateRequestThread

                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(BUFFER_SIZE)

                if not self.data:
                    break

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
                    self.handle_message()
                    handled = True
                except:
                    raise
        except socket.error, e:
            handle_socket_exception(e, self.request)
        except TerminateRequestThread:
            sys.stdout.write("Terminate thread\n")
            pass
        except:
            print "Unexpected error:", sys.exc_info
            raise
        finally:
            sys.stdout.write("Client disconnected\n")
            # Release semaphore on thread destruction
            if handled:
                semaphore.release()
