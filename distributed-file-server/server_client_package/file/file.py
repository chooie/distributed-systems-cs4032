import logging
import os
import sys
import shared_lib.message as msg

from server.server_core.request_handler import ThreadedTCPRequestHandler
from shared_lib.LocalFile import LocalFile
from shared_lib.file import send_file_from_local_to_remote, \
    send_confirmation_message_to_upload_request, download_file
from shared_lib.utils import run_server
from shared_lib.DistributedFile import DistributedFile


script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
files_path = ".files/"
abs_directory_path = os.path.join(script_dir, files_path)


class FileHandler(ThreadedTCPRequestHandler):
    files = ["lorem_ipsum_large.txt", "yin_yang.svg"]

    def handle_message(self):
        # print self.data
        message = msg.create_message_obj(self.data)

        if isinstance(message, msg.Download):
            logging.info("Processing Download Request: " + message.file_name)
            self.send_file(message.file_name, abs_directory_path)
            logging.info("Processing Download Request finished: " +
                         message.file_name)

        elif isinstance(message, msg.Upload):
            logging.info("Processing Upload Request: " + message.file_name)
            self.store_file(message.file_name, message.file_size)
            logging.info("Processing Upload Request finished: " +
                         message.file_name)

        else:
            self.request.sendall("Unrecognised message:\n" + self.data)

    def send_file(self, file_id, abs_directory_path):
        socket = self.request

        abs_file_path = os.path.join(abs_directory_path, file_id)

        f = open(abs_file_path, 'r')

        bytes_size = os.path.getsize(abs_file_path)

        local_file = LocalFile(f, file_id, abs_file_path, bytes_size)

        send_file_from_local_to_remote(local_file, socket)

        local_file.close()

    def store_file(self, file_id, file_size):
        socket = self.request

        send_confirmation_message_to_upload_request(file_id, file_size, socket)

        file_contents = download_file(file_id, file_size, socket)

        logging.info("Storing file: " + file_id)

        abs_file_path = os.path.join(abs_directory_path, file_id)

        f = open(abs_file_path, 'w+')

        f.write(file_contents)

        bytes_size = os.path.getsize(abs_file_path)

        local_file = LocalFile(f, file_id, abs_file_path, bytes_size)

        local_file.close()

        logging.info("Storing file finished: " + file_id)


if __name__ == "__main__":
    logging.basicConfig(filename='file-log.log', level=logging.DEBUG)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    run_server(FileHandler)
