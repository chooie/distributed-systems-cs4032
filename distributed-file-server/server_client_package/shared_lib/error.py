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

