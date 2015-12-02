import sys
from random import randint
from time import sleep
import errno
import socket
from ..shared_lib.error import handle_socket_exception
import threading
import client_utils as utils

BUFFER_SIZE = 1024
HOST = "0.0.0.0"
PORT_NUMBER = 8080
NUMBER_OF_CLIENTS = 20


def client_worker(ip, port, message):
    sleep(randint(1, 5))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)


def test_chat(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        message = utils.create_join_chat_room_message("cats", "charlie")
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        while True:
            sleep(randint(1, 5))
            sock.sendall(
                utils.create_leave_chat_room_message(
                    "cats", randint(1, 100), "charlie"
                )
            )
            response = sock.recv(BUFFER_SIZE)
            sys.stdout.write(response + "\n")
    except socket.error, e:
        handle_socket_exception(e, sock)


def run():
    threads = []

    # Full test scenario
    t = threading.Thread(
            target=test_chat,
            args=(HOST, PORT_NUMBER)
        )
    threads.append(t)
    t.start()

    t = threading.Thread(
            target=client_worker,
            args=(HOST, PORT_NUMBER, "HELO text\n")
        )
    threads.append(t)
    t.start()

    # # Create client, 'bill'
    # room = "programming"
    # client = "bill123"
    # message = utils.create_join_chat_room_message(room, client)
    # sys.stdout.write(message)
    # t = threading.Thread(
    #         target=client_worker,
    #         args=(HOST, PORT_NUMBER, message)
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Create client, mary
    # room = "programming"
    # client = "mary123"
    # message = utils.create_leave_chat_room_message(room, 0, client)
    # sys.stdout.write(message)
    # t = threading.Thread(
    #         target=client_worker,
    #         args=(HOST, PORT_NUMBER, message)
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Create client, jack
    # room = "programming"
    # client = "jack123"
    # message = utils.create_disconnect_chat_room_message(client)
    # sys.stdout.write(message)
    # t = threading.Thread(
    #         target=client_worker,
    #         args=(HOST, PORT_NUMBER, message)
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Create client, bobby
    # room = "programming"
    # client = "bobby123"
    # message = "Hello, world!"
    # message = utils.create_message_chat_room_message(room, 0, client, message)
    # sys.stdout.write(message)
    # t = threading.Thread(
    #         target=client_worker,
    #         args=(HOST, PORT_NUMBER, message)
    #     )
    # threads.append(t)
    # t.start()

if __name__ == "__main__":
    run()
