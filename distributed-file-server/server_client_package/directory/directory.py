import sys
import logging
import shared_lib.message as msg

from shared_lib.utils import run_server
from server.server_core.request_handler import ThreadedTCPRequestHandler
from shared_lib.constants import STATIC_HOST
from file.constants import FILE_PORT


class FileServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = []

    def add_file(self, file_name):
        self.files.append(file_name)

    def get_files(self):
        return self.files

    def check_file_on_server(self, file_name):
        for file_on_server in self.files:
            if file_on_server == file_name:
                return True
        return False


class DirectoryHandler(ThreadedTCPRequestHandler):
    file_server = FileServer(STATIC_HOST, FILE_PORT)
    file_server.add_file('lorem_ipsum_large.txt')
    file_server.add_file('yin_yang.svg')

    file_servers = [
        file_server
    ]

    def __init__(self, client_address, request, server):
        ThreadedTCPRequestHandler.__init__(self, client_address, request,
                                           server)

    def handle_message(self):
        socket = self.request

        message = msg.create_message_obj(self.data)

        if isinstance(message, msg.Connect):
            logging.info("Processing Connect Request: " + message.file_name)

            file_name = message.file_name

            file_server = self.get_file_server_by_file_name(file_name)

            direct_message = msg.create_directory_direct_message(
                file_server.host, file_server.port, file_name
            )

            socket.sendall(direct_message)

            logging.info("Processing Connect Request finished: " +
                         message.file_name)

        else:
            self.request.sendall("Unrecognised message:\n" + self.data)

    def get_file_server_by_file_name(self, file_name):
        for file_server in self.file_servers:
            if file_server.check_file_on_server(file_name):
                return file_server
        return None


if __name__ == "__main__":
    logging.basicConfig(filename='directory-log.log', level=logging.DEBUG)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    run_server(DirectoryHandler)
