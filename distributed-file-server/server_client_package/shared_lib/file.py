import logging
import os
import sys

from shared_lib import message as msg
from shared_lib.constants import BUFFER_SIZE


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


def distributed_open(file_id, abs_directory_path, socket):
    """
    Read file from file server
    :param abs_directory_path: Path to where file will be stored
    :param file_id: Unique string for file
    :param socket: Socket connection with file server
    :return: a handle to the file
    """
    send_file_download_message(file_id, socket)

    response = read_upload_response_message(file_id, socket)

    upload_message = msg.create_message_obj(response)

    file_name = upload_message.file_name

    assert file_id == file_name

    file_size = upload_message.file_size

    send_confirmation_message_to_upload_request(file_name, file_size, socket)

    file_contents = download_file(file_name, file_size, socket)

    f = prepare_file(file_name, abs_directory_path, file_contents)

    return DistributedFile(f, file_id, f.name, file_size, socket)


def send_file_download_message(file_name, socket):
    logging.info("Sending download file request: " + file_name)

    download_file_message = msg.create_download_file_message(file_name)

    socket.send(download_file_message)

    logging.info("Sending download file request finished: " + file_name)


def read_upload_response_message(file_name, socket):
    logging.info("Reading response: " + file_name)

    response = socket.recv(BUFFER_SIZE)

    logging.info("Response:\n" + response)

    logging.info("Reading response finished: " + file_name)

    return response


def send_confirmation_message_to_upload_request(file_name, file_size, socket):

    logging.info("Sending confirmation: " + file_name)

    confirmation = msg.create_file_acception_message(file_name,
                                                     file_size)
    socket.sendall(confirmation)

    logging.info("Sending confirmation finished: " + file_name)


def download_file(file_name, file_size, socket):
    logging.info("Downloading file: " + file_name)

    file_contents = ''

    while True:
        file_chunk = socket.recv(BUFFER_SIZE)

        file_contents += file_chunk

        if sys.getsizeof(file_contents) >= file_size:
            break

    logging.info("Downloading file finished: " + file_name)

    return file_contents


def prepare_file(file_id, abs_directory_path,  file_contents):
    abs_file_path = os.path.join(abs_directory_path, file_id)

    f = open(abs_file_path, 'w+')

    f.write(file_contents)

    return f
