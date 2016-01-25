import sys
from shared_lib.string import add_newline_at_end_if_missing


def write_message(base, message):
    base = add_newline_at_end_if_missing(base)
    message = add_newline_at_end_if_missing(message)
    sys.stdout.write(base + message)


def server_start(server_thread):
    message = "On thread: {0}".format(server_thread.name)
    write_message("Starting server:", message)


def processing(message):
    write_message("Processing:", message)


def error_processing(message):
    write_message("ERROR - Processing:", message)


def processed(message):
    write_message("Processed:", message)


def refused(message):
    write_message("Refused:", message)

