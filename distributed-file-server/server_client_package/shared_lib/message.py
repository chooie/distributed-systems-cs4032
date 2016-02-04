from utils import message_to_array


def create_helo_message():
    return "HELO text\n"


def create_kill_message():
    return "KILL_SERVICE\n"


def create_some_dummy_message():
    return "Hi there!"


def create_download_file_message(file_name):
    return (
        "File\n"
        "Download\n"
        "{0}\n"
    ).format(file_name)


def create_upload_file_message(file_name, file_size):
    return (
        "File\n"
        "Upload\n"
        "{0}\n"
        "{1}\n"
    ).format(file_name, file_size)


def create_file_acception_message(file_name, file_size):
    return (
        "File\n"
        "Confirm\n"
        "{0}\n"
        "{1}\n"
    ).format(file_name, file_size)


def create_message_obj(message_string):
    message_array = message_to_array(message_string)

    if len(message_array) > 1:
        domain = message_array[0]
        action_type = message_array[1]
        body = message_array[2]

        if domain == "File":
            file_name = body
            if action_type == "Download":
                return Download(domain, action_type, file_name)

            elif action_type == "Upload":
                file_size = message_array[3]
                return Upload(domain, action_type, file_name, file_size)

            elif action_type == "Confirm":
                file_size = message_array[3]
                return Confirm(domain, action_type, file_name, file_size)

    return None


class Message(object):
    def __init__(self, domain, action_type):
        self.domain = domain
        self.action_type = action_type


class FileMessage(Message):
    def __init__(self, domain, action_type, file_name):
        Message.__init__(self, domain, action_type)
        self.file_name = file_name


class Download(FileMessage):
    def __init__(self, domain, action_type, file_name):
        FileMessage.__init__(self, domain, action_type, file_name)


class FileSize(FileMessage):
    def __init__(self, domain, action_type, file_name, file_size):
        FileMessage.__init__(self, domain, action_type, file_name)
        self.file_size = int(file_size)


class Upload(FileSize):
    def __init__(self, domain, action_type, file_name, file_size):
        FileSize.__init__(self, domain, action_type, file_name, file_size)


class Confirm(FileSize):
    def __init__(self, domain, action_type, file_name, file_size):
        FileSize.__init__(self, domain, action_type, file_name, file_size)
