import errno

MESSAGE_HANDLER_ERROR = 0
DUPLICATE_CLIENT_ERROR = 1
DUPLICATE_CHAT_CLIENT_ERROR = 2
DUPLICATE_CHAT_ROOM_ERROR = 3
NON_EXISTANT_CHAT_ROOM_ERROR = 4


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


def create_error_message(error_number, error_description):
    return (
        "ERROR_CODE: {0}\n"
        "ERROR_DESCRIPTION: {1}\n"
    ).format(error_number, error_description)


class InformClientError(Exception):
    def __init__(self, error_number, error_description):
        super(InformClientError, self).__init__(error_description)
        self.error_description = error_description
        self.error_number = error_number

    def get_error_message(self):
        return create_error_message(self.error_number, self.error_description)


class MessageHandlerError(InformClientError):
    def __init__(self, original_message):
        super(MessageHandlerError, self).__init__(
             MESSAGE_HANDLER_ERROR, "There was an error handling your message"
        )
        self.original_message = original_message


class DuplicateClientError(InformClientError):
    def __init__(self, client_name=None):
        if not client_name:
            message = "There is already a user with that name"
        else:
            message = "User, '{0}', is already a member".format(client_name)
        super(DuplicateClientError, self).__init__(
            DUPLICATE_CLIENT_ERROR, message
        )


class DuplicateChatClientError(InformClientError):
    def __init__(self):
        super(DuplicateChatClientError, self).__init__(
            DUPLICATE_CHAT_CLIENT_ERROR,
            "This chat room already has a member by that name"
        )


class DuplicateChatRoomError(InformClientError):
    def __init__(self):
        super(DuplicateChatRoomError, self).__init__(
            DUPLICATE_CHAT_ROOM_ERROR,
            "This chat room already exists"
        )


class NonExistantChatRoomError(InformClientError):
    def __init__(self, chat_room_id=None):
        if chat_room_id is None:
            message = "This chat room doesn't exist"
        else:
            message = "Chat room with ID, '{0}', doesn't exist".format(
                chat_room_id,
            )
        super(NonExistantChatRoomError, self).__init__(
            NON_EXISTANT_CHAT_ROOM_ERROR,
            message
        )
