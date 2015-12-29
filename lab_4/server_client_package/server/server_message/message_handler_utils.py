from server_client_package.server.log import write_message
from server_client_package.server.server_message.message import \
    create_joined_chat_room_message, create_left_chat_room_message, \
    create_chat_message
from server_client_package.shared_lib.error import NonExistantChatRoomError


def handle_join_chat_room(values, server_thread):
    chat_room_name = values["JOIN_CHATROOM"]
    client_name = values["CLIENT_NAME"]

    chat = server_thread.chat

    chat.add_active_client(client_name, server_thread)

    chat_room = chat.add_chat_room(chat_room_name)

    client = chat.get_active_client_by_name(client_name)

    response = create_joined_chat_room_message(
        chat_room.name, chat_room.id, client.id
    )

    write_message("Handle join chat message:", response)

    server_thread.request.sendall(response)

    write_message("Message sent to client", '')

    chat_room.add_member(client)


def handle_leave_chat_room(values, server_thread):
    chat_room_id = values["LEAVE_CHATROOM"]
    client_id = values["JOIN_ID"]
    client_name = values["CLIENT_NAME"]

    chat = server_thread.chat

    chat_room = chat.get_chat_room_by_id(chat_room_id)

    if chat_room is None:
        raise NonExistantChatRoomError(chat_room_id)

    client_by_id = chat_room.get_member_by_id(client_id)
    client_by_name = chat_room.get_member_by_name(client_name)

    if client_by_id != client_by_name:
        write_message("Error:", "Client ID and Name don't match!")
        raise Exception

    chat_room.remove_member(client_by_id)

    response = create_left_chat_room_message(values)

    write_message("Handle leave chat message:", response)

    server_thread.request.sendall(response)


def handle_disconnect(values, server_thread):
    client_name = values["CLIENT_NAME"]

    chat = server_thread.chat

    write_message("Handling disconnect...", '')

    chat.remove_active_client(client_name)


def handle_chat(values, server_thread):
    chat_room_name = values["CHAT"]

    response = create_chat_message(values)

    write_message("Handle chat message:", response)

    chat = server_thread.chat

    chat_room = chat.get_chat_room_by_name(chat_room_name)

    chat_room.send_message_to_all_members(response)
