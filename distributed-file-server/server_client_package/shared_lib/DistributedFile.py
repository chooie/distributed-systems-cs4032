import socket
import shared_lib.message as msg

from shared_lib.LocalFile import LocalFile
from shared_lib.file import send_file_download_message, \
    establish_file_directory, read_upload_response_message, \
    send_confirmation_message_to_upload_request, download_file, \
    string_to_file, send_file_from_local_to_remote


class DistributedFile(LocalFile):
    def __init__(self, file_handle, file_name, abs_path, bytes_size,
                 file_server_socket):
        LocalFile.__init__(self, file_handle, file_name, abs_path, bytes_size)
        self.file_server_socket = file_server_socket

    def close(self):
        send_file_from_local_to_remote(self, self.file_server_socket)
        self.file_server_socket.close()

    def final_close(self):
        return self.file_handle.close()

    @staticmethod
    def open(file_id, abs_directory_path, directory_socket):
        """
        Read file from file server
        :param abs_directory_path: Path to where file will be stored
        :param file_id: Unique string for file
        :param directory_socket: Socket connection with file server
        :return: a handle to the file
        """
        file_server_message = establish_file_directory(file_id,
                                                       directory_socket)

        host = file_server_message.host
        port = file_server_message.port

        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        file_socket.connect((host, port))

        send_file_download_message(file_id, file_socket)

        response = read_upload_response_message(file_id, file_socket)

        file_name = response.file_name

        assert file_id == file_name

        file_size = response.file_size

        send_confirmation_message_to_upload_request(file_name, file_size,
                                                    file_socket)

        file_contents = download_file(file_name, file_size, file_socket)

        f = string_to_file(file_name, abs_directory_path, file_contents)

        return DistributedFile(f, file_id, f.name, file_size, file_socket)
