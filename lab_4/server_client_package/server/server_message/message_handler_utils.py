from server_client_package.server.server_message.message import \
    create_joined_chat_room_message, create_left_chat_room_message, \
    create_chat_message


def handle_join_chat_room(values, request):
    response = create_joined_chat_room_message(values)

    # TODO: join

    request.sendall(response)


def handle_leave_chat_room(values, request):
    response = create_left_chat_room_message(values)

    # TODO: Leave chat room
    request.sendall(response)


def handle_disconnect(values, request):
    client_name = values["CLIENT_NAME"]

    # TODO: Disconnect client with 'client_name'


def handle_chat(values, request):
    response = create_chat_message(values)
    request.sendall(response)
