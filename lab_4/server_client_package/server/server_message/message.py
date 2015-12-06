from collections import OrderedDict
from server_client_package.shared_lib.string import \
    add_newline_at_end_if_missing


def create_joined_chat_room_message(values):
    chat_room_name = values["JOIN_CHATROOM"]

    # TODO: come up with way of creating ids
    chat_room_id = "12345"
    client_id = "54321"
    return (
            "JOINED_CHATROOM: {0}\n"
            "SERVER_IP: 0\n"
            "PORT: 0\n"
            "ROOM_REF: {1}\n"
            "JOIN_ID: {2}\n"
        ).format(chat_room_name, chat_room_id, client_id)


def create_left_chat_room_message(values):
    chat_room_id = values["LEAVE_CHATROOM"]
    client_id = values["JOIN_ID"]
    return (
        "LEFT_CHATROOM: {0}\n"
        "JOIN_ID: {1}\n"
    ).format(chat_room_id, client_id)


def create_chat_message(values):
    chat_room_id = values["CHAT"]
    client_name = values["CLIENT_NAME"]
    message = add_newline_at_end_if_missing(values["MESSAGE"])
    return (
        "CHAT: {0}\n"
        "CLIENT_NAME: {1}\n"
        "MESSAGE: {2}\n"
    ).format(chat_room_id, client_name, message)


def message_to_dict(message):
    message_dict = OrderedDict()
    message_lines = message.split('\n')

    # Remove empty elements
    message_lines = filter(None, message_lines)
    for message_line in message_lines:
        line_words = message_line.split(':')
        line_words = map(lambda x: x.strip(), line_words)

        key = line_words[0]
        value = line_words[1]

        message_dict[key] = value
    return message_dict


def get_message_dict_type(values):
    return values.keys()[0]