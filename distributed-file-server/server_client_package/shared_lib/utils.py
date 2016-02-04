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


def message_to_array(message):
    return remove_empty_elements(message.split("\n"))


def remove_empty_elements(arr):
    return filter(None, arr)


def remove_whitespace_from_elements(arr):
    return map(lambda x: x.strip(), arr)
