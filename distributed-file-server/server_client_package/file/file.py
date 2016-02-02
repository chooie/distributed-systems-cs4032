import logging
import os

from server.server_core.request_handler import ThreadedTCPRequestHandler
from shared_lib.utils import run_server
from shared_lib.utils import parse_message

script_dir = os.path.dirname(__file__)  # Absolute dir the script is in


class FileHandler(ThreadedTCPRequestHandler):
    files = ["lorem_ipsum_large.txt", "yin_yang.svg"]

    def handle_message(self):
        # print self.data
        message_array = parse_message(self.data)

        if len(message_array) > 1:
            domain = message_array[0]
            action_type = message_array[1]
            body = message_array[2]

            if domain == "File":
                if action_type == "Open":
                    if body in self.files:
                        print body
                        self.send_file(body)

        else:
            self.request.sendall("Unrecognised message:\n" + self.data)

    def send_file(self, file_id):
        """
        Read file from file server
        :param file_id: Unique string for file
        :return: a handle to the file
        """

        print "Sending file..."

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
