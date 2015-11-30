def create_joined_chat_room_message(chat_room_name, chat_room_id, client_id):
    return (
            "JOINED_CHATROOM: {0}\n"
            "SERVER_IP: 0\n"
            "PORT: 0\n"
            "ROOM_REF: {1}\n"
            "JOIN_ID: {2}\n"
        ).format(chat_room_name, chat_room_id, client_id)


def process_message(message):
    message_array = message.split('\n')
    print message_array
