import sys

class LocalFile:
    def __init__(self, file_handle, file_name, abs_path, bytes_size):
        """
        Local File
        :param file_handle:
        :param file_name:
        :param abs_path:
        :param bytes_size:
        :return:
        """
        self.file_handle = file_handle
        self.file_name = file_name
        self.abs_path = abs_path
        self.bytes_size = bytes_size

    def read(self):
        f = self.file_handle
        f.seek(0)
        return f.read()

    def write(self, content):
        f = self.file_handle
        f.seek(0)
        f.truncate()
        self.bytes_size = sys.getsizeof(content)
        return f.write(content)

    def close(self):
        return self.file_handle.close()
