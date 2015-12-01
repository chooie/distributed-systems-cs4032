def create_joined_chat_room_message(chat_room_name, chat_room_id, client_id):
    return (
            "JOINED_CHATROOM: {0}\n"
            "SERVER_IP: 0\n"
            "PORT: 0\n"
            "ROOM_REF: {1}\n"
            "JOIN_ID: {2}\n"
        ).format(chat_room_name, chat_room_id, client_id)


def is_chat_join_message(message):
    message_lines = message.split('\n')
    return message_lines[0].split(':')[0] == "JOIN_CHATROOM"


def message_to_dict(message):
    message_dict = dict()
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


def process_message(message):

    values = message_to_dict(message)

    # TODO recognise message type
    if values.get("JOIN_CHATROOM"):
        print "JOIN REQUEST"
    elif values.get("LEAVE_CHATROOM"):
        print "LEAVE REQUEST"
    elif values.get("DISCONNECT"):
        print "DISCONNECT REQUEST"
    elif values.get("CHAT"):
        print "CHAT REQUEST"
