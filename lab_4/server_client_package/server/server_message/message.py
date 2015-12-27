from collections import OrderedDict
from server_client_package.shared_lib.string import \
    add_newline_at_end_if_missing
from server_client_package.shared_lib.constants import HOST, PORT


def create_joined_chat_room_message(values):
    chat_room_name = values["JOIN_CHATROOM"]

    # TODO: come up with way of creating ids
    chat_room_id = "12345"
    client_id = "54321"
    return (
            "JOINED_CHATROOM: {0}\n"
            "SERVER_IP: {1}\n"
            "PORT: {2}\n"
            "ROOM_REF: {3}\n"
            "JOIN_ID: {4}\n"
        ).format(chat_room_name, HOST, PORT, chat_room_id, client_id)


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


def remove_empty_elements(arr):
    return filter(None, arr)


def remove_whitespace_from_elements(arr):
    return map(lambda x: x.strip(), arr)


def message_to_dict(message):
    message_dict = OrderedDict()
    message_lines = message.split('\n')

    # Remove empty elements
    message_lines = remove_empty_elements(message_lines)
    for message_line in message_lines:
        line_words = message_line.split(':')
        line_words = remove_whitespace_from_elements(line_words)

        key = line_words[0]
        value = line_words[1]

        message_dict[key] = value
    return message_dict


def get_message_dict_type(values):
    return values.keys()[0]
