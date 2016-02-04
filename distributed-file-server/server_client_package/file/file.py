import logging
import os
import sys
import shared_lib.message as msg

from server.server_core.request_handler import ThreadedTCPRequestHandler
from shared_lib.utils import run_server
from shared_lib.constants import BUFFER_SIZE


script_dir = os.path.dirname(__file__)  # Absolute dir the script is in


class FileHandler(ThreadedTCPRequestHandler):
    files = ["lorem_ipsum_large.txt", "yin_yang.svg"]

    def handle_message(self):
        # print self.data
        message = msg.create_message_obj(self.data)

        if isinstance(message, msg.Download):
            self.send_file(message.file_name)

        elif isinstance(message, msg.Upload):
            self.store_file(message.file_name, message.file_size)

        else:
            self.request.sendall("Unrecognised message:\n" + self.data)

    def send_file(self, file_id):
        """
        Read file from file server
        :param file_id: Unique string for file
        :return: a handle to the file
        """
        socket = self.request

        rel_path = ".files/" + file_id

        abs_file_path = os.path.join(script_dir, rel_path)

        f = open(abs_file_path, 'r')

        file_contents = f.read()

        file_size = os.path.getsize(abs_file_path)

        logging.info("Sending file write request: " + file_id)

        request_message = msg.create_upload_file_message(file_id, file_size)

        socket.sendall(request_message)

        logging.info("Sending file write request finished: " + file_id)

        logging.info("Reading confirmation message: " + file_id)

        confirmation_message = socket.recv(BUFFER_SIZE)

        logging.info(confirmation_message)

        logging.info("Reading confirmation message finished: " + file_id)



        logging.info("Sending file: " + file_id)

        socket.sendall(file_contents)

        logging.info("Sending file finished: " + file_id)

        f.close()

    def store_file(self, file_id, file_size):
        socket = self.request

        rel_path = ".files/" + file_id

        abs_file_path = os.path.join(script_dir, rel_path)

        logging.info("Downloading file: " + file_id)

        with open(abs_file_path, 'w') as f:
            file_contents = ''

            while True:
                file_chunk = socket.recv(BUFFER_SIZE)
                logging.info(file_chunk)

                if file_chunk == "END_FILE":
                    break

                file_contents += file_chunk

            f.write(file_contents)

        logging.info("Downloading file finished: " + file_id)


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
