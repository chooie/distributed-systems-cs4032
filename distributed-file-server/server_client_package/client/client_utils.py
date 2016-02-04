import socket
import sys
import file

from shared_lib.constants import BUFFER_SIZE
from shared_lib.error import handle_socket_exception


def execute_scenario(ip, port, message_f):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    message = message_f()
    try:
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)


def file_scenario(ip, port, file_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        f = file.open_file(file_name, sock)
        # f.write("HELLO THERE!")
        # f.close()
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)
