import sys
from server.server_core.server_core import run


def safe(lock, f):
    lock.acquire()
    output = f()
    lock.release()
    return output


def run_server(handler):
    host = sys.argv[1]
    port = int(sys.argv[2])
    run(host, port, handler)
