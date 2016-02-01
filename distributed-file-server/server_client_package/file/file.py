import logging
import os

from server.server_core.request_handler import ThreadedTCPRequestHandler
from shared_lib.utils import run_server
from shared_lib.constants import BUFFER_SIZE

script_dir = os.path.dirname(__file__)  # Absolute dir the script is in


class FileHandler(ThreadedTCPRequestHandler):
    files = ["lorem_ipsum_large.txt", "yin_yang.svg"]

    def handle_message(self):
        print "I'm a file handler!"
        # print self.data

        if self.data in self.files:
            self.send_file(self.data)

        else:
            self.request.sendall("Unrecognised message")

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

        print file_contents

        socket.sendall(file_contents)

        socket.send("END_FILE")

        print "Finished sending file..."

        f.close()


if __name__ == "__main__":
    logging.basicConfig(filename='file-log.log', level=logging.DEBUG)

    run_server(FileHandler)
