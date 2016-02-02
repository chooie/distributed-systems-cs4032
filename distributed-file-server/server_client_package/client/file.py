import os
import logging

from shared_lib.constants import BUFFER_SIZE
from message import create_open_file_message


script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
files_path = ".files/"


class DistributedFile:
    def __init__(self, file_handle, socket):
        """
        Distributed File
        :param file_handle: A reference to a native Python file IO object
        :param socket: The socket associated with the file server
        :return:
        """
        self.file_handle = file_handle
        self.socket = socket

    def read(self):
        self.file_handle.seek(0)
        return self.file_handle.read()

    def write(self, content):
        f = self.file_handle
        f.seek(0)
        f.truncate()
        return f.write(content)

    def close(self, file_id, socket):
        pass


def open_file(file_id, socket):
    """
    Read file from file server
    :param file_id: Unique string for file
    :param socket: Socket connection with file server
    :return: a handle to the file
    """

    open_file_message = create_open_file_message(file_id)

    socket.send(open_file_message)

    rel_path = files_path + file_id
    abs_file_path = os.path.join(script_dir, rel_path)

    f = open(abs_file_path, 'w+')

    logging.info("Downloading file...")

    file_contents = ''

    while True:
        file_chunk = socket.recv(BUFFER_SIZE)

        if file_chunk == "END_FILE":
            break

        file_contents += file_chunk

    f.write(file_contents)
    logging.info("Downloading finished...")

    return DistributedFile(f, socket)
