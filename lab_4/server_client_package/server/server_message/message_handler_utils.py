import sys

from server_client_package.server.server_message.message import \
    create_joined_chat_room_message, create_left_chat_room_message, \
    create_chat_message
from server_client_package.server.server_core.server_utils import \
    TerminateRequestThread
from server_client_package.shared_lib.error import NonExistantChatRoomError


def handle_join_chat_room(values, server_thread):
    # Placeholder
    client_id = 0
    chat_room_name = values["JOIN_CHATROOM"]
    client_name = values["CLIENT_NAME"]

    chat = server_thread.chat

    chat.add_active_client(client_name, client_id, server_thread)

    chat_room = chat.add_chat_room(chat_room_name)

    chat_room.add_member(client_name, client_id)

    response = create_joined_chat_room_message(values)

    server_thread.request.sendall(response)


def handle_leave_chat_room(values, server_thread):
    chat_room_name = values["LEAVE_CHATROOM"]
    client_id = values["JOIN_ID"]
    client_name = values["CLIENT_NAME"]

    chat = server_thread.chat

    chat_room = chat.get_chat_room(chat_room_name)

    if not chat_room:
        raise NonExistantChatRoomError()

    chat_room.remove_member(client_name, client_id)

    response = create_left_chat_room_message(values)

    server_thread.request.sendall(response)


def handle_disconnect(values, server_thread):
    client_name = values["CLIENT_NAME"]

    # TODO: Disconnect client with 'client_name'
    raise TerminateRequestThread()


def handle_chat(values, server_thread):
    response = create_chat_message(values)
    server_thread.request.sendall(response)
