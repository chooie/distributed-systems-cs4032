from functools import partial
from collections import OrderedDict


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


def message_to_dict(message):
    message_dict = OrderedDict()
    message_lines = message.split('\n')

    # Remove last newline
    message_lines = message_lines[:-1]
    for message_line in message_lines:
        line_words = message_line.split(':')
        line_words = map(lambda x: x.strip(), line_words)

        key = line_words[0]
        value = line_words[1]

        message_dict[key] = value
    return message_dict


def get_message_dict_type(values):
    print values.keys()
    return values.keys()[0]


def do_nothing():
    return "DEFAULT"


def create_response_message_from_type(message):
    values = message_to_dict(message)

    ops = {
        "JOIN_CHATROOM": partial(create_joined_chat_room_message, values),
        "LEAVE_CHATROOM": partial(do_nothing),
        "DISCONNECT": partial(do_nothing),
        "CHAT": partial(do_nothing)
    }

    message_type = get_message_dict_type(values)

    response = ops[message_type]()

    print response


def process_message(message):
    response = create_response_message_from_type(message)
