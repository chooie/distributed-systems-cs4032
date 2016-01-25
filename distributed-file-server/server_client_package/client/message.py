def create_helo_message():
    return "HELO text\n"


def create_bad_message():
    return "This is a bad message"


def create_join_chat_room_message(chat_room_name, client_name):
    return (
        "JOIN_CHATROOM: {0}\n"
        "CLIENT_IP: 0\n"
        "PORT: 0\n"
        "CLIENT_NAME: {1}\n"
    ).format(chat_room_name, client_name)


def create_leave_chat_room_message(chat_room_name, join_id, client_name):
    return (
        "LEAVE_CHATROOM: {0}\n"
        "JOIN_ID: {1}\n"
        "CLIENT_NAME: {2}\n"
    ).format(chat_room_name, join_id, client_name)


def create_disconnect_message(client_name):
    return (
        "DISCONNECT: 0\n"
        "PORT: 0\n"
        "CLIENT_NAME: {0}\n"
    ).format(client_name)


def create_message_chat_room_message(chat_room_name, join_id, client_name,
                                     message):
    return (
        "CHAT: {0}\n"
        "JOIN_ID: {1}\n"
        "CLIENT_NAME: {2}\n"
        "MESSAGE: {3}\n"
    ).format(chat_room_name, join_id, client_name, message)
