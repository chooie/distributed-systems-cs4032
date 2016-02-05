import shared_lib.message as msg

from shared_lib.LocalFile import LocalFile
from shared_lib.file import send_file_download_message, \
    read_upload_response_message, send_confirmation_message_to_upload_request, \
    download_file, string_to_file, send_file_from_local_to_remote


class DistributedFile(LocalFile):
    def __init__(self, file_handle, file_name, abs_path, bytes_size, socket):
        LocalFile.__init__(self, file_handle, file_name, abs_path, bytes_size)
        self.socket = socket

    def close(self):
        send_file_from_local_to_remote(self, self.socket)

    def final_close(self):
        return self.file_handle.close()

    @staticmethod
    def open(file_id, abs_directory_path, socket):
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

        send_confirmation_message_to_upload_request(file_name, file_size,
                                                    socket)

        file_contents = download_file(file_name, file_size, socket)

        f = string_to_file(file_name, abs_directory_path, file_contents)

        return DistributedFile(f, file_id, f.name, file_size, socket)
