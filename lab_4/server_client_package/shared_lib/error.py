import errno

MESSAGE_HANDLER_ERROR = 0
DUPLICATE_CLIENT_ERROR = 1


def handle_socket_exception(error, socket):
    if isinstance(error.args, tuple):
        print "Error number is %d" % error[0]
        if error[0] == errno.EPIPE:
            # Remote peer disconnected
            print "Detected remote disconnect"
        else:
            # Determine and handle different error
            print "An error occurred with a socket"
            pass
    else:
        print "Socket error ", error
    socket.close()


class MessageHandlerError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(MessageHandlerError, self).__init__(message)

    @staticmethod
    def get_error_message():
        return create_error_message(
            MESSAGE_HANDLER_ERROR, "There was an error handling your message"
        )


class DuplicateClientError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(DuplicateClientError, self).__init__(message)

    @staticmethod
    def get_error_message():
        return create_error_message(
            DUPLICATE_CLIENT_ERROR, "There is already a user with that name"
        )


def create_error_message(error_number, error_description):
    return (
        "ERROR_CODE: {0}\n"
        "ERROR_DESCRIPTION: {1}\n"
    ).format(error_number, error_description)