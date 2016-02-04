import logging
import os
import sys
import shared_lib.message as msg

from shared_lib.constants import BUFFER_SIZE

script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
files_path = ".files/"


class DistributedFile:
    def __init__(self, file_handle, file_id, abs_file_path, file_size, socket):
        """
        Distributed File
        :param file_handle: A reference to a native Python file IO object
        :param socket: The socket associated with the file server
        :return:
        """
        self.file_handle = file_handle
        self.file_id = file_id
        self.abs_file_path = abs_file_path
        self.file_size = file_size
        self.socket = socket

    def read(self):
        self.file_handle.seek(0)
        return self.file_handle.read()

    def write(self, content):
        f = self.file_handle
        f.seek(0)
        f.truncate()
        return f.write(content)

    # def close(self):
    #     close_file_message = create_close_file_message(self.file_id,
    #                                                    self.file_size)
    #
    #     self.socket.send(close_file_message)
    #
    #     logging.info("Uploading file: " + self.file_id)
    #
    #     f = self.file_handle
    #
    #     f.seek(0)
    #     file_contents = f.read()
    #
    #     logging.info("Close file: " + file_contents)
    #
    #     self.socket.sendall(file_contents)
    #
    #     logging.info("Uploading file finished: " + self.file_id)


def open_file(file_id, socket):
    """
    Read file from file server
    :param file_id: Unique string for file
    :param socket: Socket connection with file server
    :return: a handle to the file
    """
    logging.info("Sending download file request: " + file_id)

    download_file_message = msg.create_download_file_message(file_id)

    socket.send(download_file_message)

    logging.info("Sending download file request finished: " + file_id)

    logging.info("Reading response: " + file_id)

    response = socket.recv(BUFFER_SIZE)

    logging.info("Response:\n" + response)

    upload_message = msg.create_message_obj(response)

    file_name = upload_message.file_name
    file_size = upload_message.file_size

    logging.info("Reading response finished: " + file_id)

    logging.info("Sending confirmation: " + file_id)

    confirmation = msg.create_file_acception_message(file_name,
                                                     file_size)

    socket.sendall(confirmation)

    logging.info("Sending confirmation finished: " + file_id)

    logging.info("Downloading file: " + file_id)

    file_contents = ''

    while True:
        file_chunk = socket.recv(BUFFER_SIZE)

        file_contents += file_chunk

        if sys.getsizeof(file_contents) >= file_size:
            break

    rel_path = files_path + file_id
    abs_file_path = os.path.join(script_dir, rel_path)

    f = open(abs_file_path, 'w+')

    f.write(file_contents)

    logging.info("Downloading file finished: " + file_id)

    return DistributedFile(f, file_id, abs_file_path, file_size, socket)
