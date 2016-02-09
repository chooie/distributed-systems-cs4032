import logging
import os
import sys

from shared_lib import message as msg
from shared_lib.constants import BUFFER_SIZE


def establish_file_directory(file_name, socket):
    send_directory_connect_message(file_name, socket)

    return read_directory_direct_message(socket)


def send_directory_connect_message(file_name, socket):
    logging.info("Sending directory connect message: " + file_name)

    message = msg.create_directory_connect_message(file_name)

    socket.sendall(message)

    logging.info("Sending directory connect message finished: " + file_name)


def read_directory_direct_message(socket):
    logging.info("Sending directory direct message")

    response = socket.recv(BUFFER_SIZE)
    message = msg.create_message_obj(response)

    assert isinstance(message, msg.Direct)

    logging.info("Sending directory direct message finished")

    return message


def send_file_download_message(file_name, socket):
    logging.info("Sending download file request: " + file_name)

    download_file_message = msg.create_download_file_message(file_name)

    socket.sendall(download_file_message)

    logging.info("Sending download file request finished: " + file_name)


def send_file_upload_message(file_name, file_size, socket):
    logging.info("Sending upload file request: " + file_name)

    upload_file_message = msg.create_upload_file_message(file_name,
                                                         file_size)
    socket.sendall(upload_file_message)

    logging.info("Sending upload file request finished: " + file_name)


def read_upload_response_message(file_name, socket):
    logging.info("Reading response: " + file_name)

    response = socket.recv(BUFFER_SIZE)

    message = msg.create_message_obj(response)

    logging.info("Upload Response:\n" + response)

    assert isinstance(message, msg.Upload)

    logging.info("Reading response finished: " + file_name)

    return message


def send_confirmation_message_to_upload_request(file_name, file_size, socket):
    logging.info("Sending confirmation: " + file_name)

    confirmation = msg.create_file_acception_message(file_name,
                                                     file_size)
    socket.sendall(confirmation)

    logging.info("Sending confirmation finished: " + file_name)


def read_confirmation_message(file_name, socket):
    logging.info("Reading confirmation message: " + file_name)

    response = socket.recv(BUFFER_SIZE)

    message = msg.create_message_obj(response)

    logging.info("Confirmation Message:\n" + response)

    assert isinstance(message, msg.Confirm)

    logging.info("Reading confirmation message finished: " + file_name)


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


def string_to_file(file_id, abs_directory_path, file_contents):
    abs_file_path = os.path.join(abs_directory_path, file_id)

    f = open(abs_file_path, 'w+')

    f.write(file_contents)

    return f


def upload_file(file_name, file_contents, socket):
    logging.info("Uploading file: " + file_name + " - " +
                 str(sys.getsizeof(file_contents)))
    logging.info(file_contents)

    socket.sendall(file_contents)

    logging.info("Uploading file finished: " + file_name)


def send_file_from_local_to_remote(file_obj, socket):
    send_file_upload_message(file_obj.file_name, file_obj.bytes_size, socket)

    read_confirmation_message(file_obj.file_name, socket)

    upload_file(file_obj.file_name, file_obj.read(), socket)
