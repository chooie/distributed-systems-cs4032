def create_helo_message():
    return "HELO text\n"


def create_kill_message():
    return "KILL_SERVICE\n"


def create_some_dummy_message():
    return "Hi there!"


def create_read_file_message(file_name):
    return (
        "File\n"
        "Read\n"
        "{0}\n"
    ).format(file_name)
