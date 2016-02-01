import threading
import SocketServer
import server_utils as utils

from server import log


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 100
    allow_reuse_address = True


def run(host, port, handler):
    server = None
    try:
        server = ThreadedTCPServer((host, port), handler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        log.server_start(server_thread)

        while True:
            # Loop until server shut down
            pass
    except (KeyboardInterrupt, SystemExit):
        utils.clean_up_server(server)
