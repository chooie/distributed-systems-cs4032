import sys
import os
import Queue
import SocketServer
from my_utils import formatDataToMessage, checkIfKillCommand

BUFFER_SIZE = 1024
HOST = "0.0.0.0"
PORT_NUMBER = 8080
STUDENT_NUMBER = 1234567890

MAX_NUM_OF_THREADS = 10

# TODO: Implement thread pool

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(BUFFER_SIZE)

        if checkIfKillCommand(self.data):
            os._exit(0)

        # Create worker thread
        t = threading.Thread(
            target = serverWorker,
            args = (HOST, PORT_NUMBER, message)
        )
        t.start()

        response = formatDataToMessage(
            self.data, HOST, PORT_NUMBER, STUDENT_NUMBER
        )

        # Respond to client
        self.request.sendall(response)

if __name__ == "__main__":

    try:
        server = SocketServer.TCPServer((HOST, PORT_NUMBER), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print "Starting Server"
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit
