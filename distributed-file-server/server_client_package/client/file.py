import os
import logging

from shared_lib.constants import BUFFER_SIZE
from message import create_read_file_message


script_dir = os.path.dirname(__file__)  # Absolute dir the script is in


def read_file(file_id, socket):
    """
    Read file from file server
    :param file_id: Unique string for file
    :param socket: Socket connection with file server
    :return: a handle to the file
    """

    read_file_message = create_read_file_message(file_id)

    socket.send(read_file_message)

    rel_path = ".files/" + file_id
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, 'w') as f:

        logging.info("Downloading file...")

        file_contents = ''

        while True:
            file_chunk = socket.recv(BUFFER_SIZE)

            if file_chunk == "END_FILE":
                break

            file_contents += file_chunk

        f.write(file_contents)
        logging.info("Downloading finished...")
    return f


def write_file(file_id, socket):
    f = open(file_id, 'wb')


def open_file(file_id, socket):
    pass


def close_file(file_id, socket):
    pass
