import sys
import socket
import threading
import client_utils as utils

from random import randint
from time import sleep
from functools import partial
from server_client_package.shared_lib.error import handle_socket_exception
from server_client_package.shared_lib.constants import BUFFER_SIZE, HOST, PORT


def helo_scenario(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sleep(randint(1, 5))
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)


def disconnect_scenario(ip, port):
    disconnect = partial(utils.create_disconnect_message, 'bill')
    utils.execute_scenario(ip, port, disconnect)


def join_chat_scenario(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        message = utils.create_join_chat_room_message("cats", "charlie")
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)


def run():
    threads = []

    # HELO scenario
    t = threading.Thread(
            target=helo_scenario,
            args=(HOST, PORT, "HELO text\n")
        )
    threads.append(t)
    t.start()

    # Disconnect scenario
    t = threading.Thread(
            target=disconnect_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

    # Test join chat room
    t = threading.Thread(
            target=join_chat_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

if __name__ == "__main__":
    run()
