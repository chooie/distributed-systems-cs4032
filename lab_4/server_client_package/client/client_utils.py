import socket
import sys
from random import randint
from time import sleep

from server_client_package.client.message import \
    create_join_chat_room_message, create_leave_chat_room_message, \
    create_disconnect_message, create_message_chat_room_message
from server_client_package.shared_lib.constants import BUFFER_SIZE
from server_client_package.shared_lib.error import handle_socket_exception


def execute_scenario(ip, port, message_f):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    message = message_f()
    try:
        sleep(randint(1, 5))
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
        sock.close()
    except socket.error, e:
        handle_socket_exception(e, sock)


def connect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock


def bill_scenario(ip, port):
    sock = connect(ip, port)

    chat_room = "cats"
    client_name = "bill"

    try:
        message = create_join_chat_room_message(chat_room, client_name)
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")

        while True:
            response = sock.recv(BUFFER_SIZE)
            sys.stdout.write(response + "\n")
            break

        sleep(2)

        message = create_leave_chat_room_message(0, 0, client_name)
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")

        sleep(2)

        message = create_disconnect_message(client_name)
        sock.sendall(message)
    except socket.error, e:
        handle_socket_exception(e, sock)


def charlie_scenario(ip, port):
    sock = connect(ip, port)

    chat_room = "cats"
    client_name = "charlie"

    scenario_executed = False

    try:
        while True:
            if scenario_executed:
                break
            message = create_join_chat_room_message(chat_room, client_name)
            sock.sendall(message)
            response = sock.recv(BUFFER_SIZE)
            sys.stdout.write(response + "\n")

            message = create_message_chat_room_message(
                chat_room, 0, client_name, "This is a test message."
            )
            sock.sendall(message)
            response = sock.recv(BUFFER_SIZE)
            sys.stdout.write(response + "\n")

            sleep(4)

            message = create_leave_chat_room_message(0, 0, client_name)
            sock.sendall(message)
            response = sock.recv(BUFFER_SIZE)
            sys.stdout.write(response + "\n")

            sleep(4)

            message = create_disconnect_message(client_name)
            sock.sendall(message)
            scenario_executed = True
    except socket.error, e:
        handle_socket_exception(e, sock)
