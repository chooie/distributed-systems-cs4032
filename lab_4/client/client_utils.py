def create_join_chat_room_message(chat_room_name, client_name):
    return (
            "JOIN_CHATROOM: {0}\n"
            "CLIENT_IP: 0\n"
            "PORT: 0\n"
            "CLIENT_NAME: {1}\n"
        ).format(chat_room_name, client_name)
