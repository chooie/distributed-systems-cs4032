import threading
import server_utils as utils

from server_client_package.server import log
from server_client_package.server.server_core.request_handler import \
    ThreadedTCPRequestHandler, ThreadedTCPServer
from server_client_package.shared_lib.constants import HOST, PORT


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
