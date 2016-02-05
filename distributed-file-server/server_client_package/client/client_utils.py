import os
import sys
import socket
import shared_lib.file

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
        script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
        files_path = ".files/"

        abs_directory_path = os.path.join(script_dir, files_path)

        f = shared_lib.file.distributed_open(file_name, abs_directory_path,
                                             sock)
        # f.write("HELLO THERE!")
        # f.close()
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)
