import sys
import os
import threading
import SocketServer
from my_utils import isKillCommand
from server_worker import serverWorker

BUFFER_SIZE = 1024
HOST = "46.101.58.11"
PORT = 80
MAX_NUMBER_OF_CLIENTS = 10
DO_NOT_BLOCK = False

# If semaphore blocks, client's connection will be refused
semaphore = threading.BoundedSemaphore(MAX_NUMBER_OF_CLIENTS)

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(BUFFER_SIZE)

        processingStr = "Processing Request:\n{0}"
        refusalStr = "Refused:\n{0}"

        if self.data[-2:] != "\n":
            processingStr += "\n"
            refusalStr += "\n"

        sys.stdout.write(processingStr.format(self.data))
        if isKillCommand(self.data):
            sys.stdout.write("Kill Request!")
            os._exit(0)

        # Attempt to acquire semaphore
        if (not semaphore.acquire(DO_NOT_BLOCK)):
            sys.stdout.write(refusalStr.format(self.data))
            self.request.send("Connection Refused\n")
            self.request.close();
            return;

        # Do Work
        serverWorker(HOST, PORT, self, semaphore)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 100
    allow_reuse_address = True
    pass

if __name__ == "__main__":

    try:
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print "Server loop running in thread:", server_thread.name
        while True:
            #loop forever
            pass
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        sys.exit
