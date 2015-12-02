import sys
import socket
from random import randint
from time import sleep
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


def create_join_chat_room_message(chat_room_name, client_name):
    return (
        "JOIN_CHATROOM: {0}\n"
        "CLIENT_IP: 0\n"
        "PORT: 0\n"
        "CLIENT_NAME: {1}\n"
    ).format(chat_room_name, client_name)


def create_leave_chat_room_message(chat_room_name, join_id, client_name):
    return (
        "LEAVE_CHATROOM: {0}\n"
        "JOIN_ID: {1}\n"
        "CLIENT_NAME: {2}\n"
    ).format(chat_room_name, join_id, client_name)


def create_disconnect_message(client_name):
    return (
        "DISCONNECT: 0\n"
        "PORT: 0\n"
        "CLIENT_NAME: {0}\n"
    ).format(client_name)


def create_message_chat_room_message(chat_room_name, join_id, client_name,
                                     message):
    # TODO: Add newline to message if not present

    return (
        "CHAT: {0}\n"
        "JOIN_ID: {1}\n"
        "CLIENT_NAME: {2}\n"
        "MESSAGE: {3}\n"
    ).format(chat_room_name, join_id, client_name, message)
