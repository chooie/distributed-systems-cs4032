from threading import Lock
from functools import partial
from chat_room import ChatRoom
from member_client import Client
from server_client_package.shared_lib.error import NonExistantChatRoomError
from server_client_package.shared_lib.utils import safe


class Chat:
    def __init__(self):
        # { 'client_id': member_obj }
        self.active_clients = {}
        # { 'chat_room_id': chat_room_obj }
        self.chat_rooms = {}
        self.active_clients_lock = Lock()
        self.chat_rooms_lock = Lock()

    def add_active_client(self, client_name, thread_handle):

        def f():
            # Add if client isn't already in dict
            if not self.get_active_client_by_name(client_name):
                # Add client
                client_obj = Client(client_name, [], thread_handle)
                self.active_clients[client_obj.id] = client_obj

            # Do nothing if they're already a member
            # raise DuplicateClientError(client_name)

        safe(self.active_clients_lock, partial(f))

    def remove_active_client(self, client_name):
        def f():
            client = self.get_active_client_by_name(client_name)

            # Loop through chat rooms and remove client
            for chat_room in client.chat_rooms:
                print "Chat Rooms:"
                print client.chat_rooms
                chat_room.remove_member(client)

            client.thread_handle.terminate_request = True

            self.active_clients.pop(client.id)

        def g():
            safe(self.chat_rooms_lock, partial(f))

        safe(self.active_clients_lock, partial(g))

    def get_active_client_by_name(self, name):
        for client_id in self.active_clients:
            client = self.active_clients.get(client_id)
            if client.name == name:
                return client
        return None

    def get_active_client_by_id(self, client_id):
        return self.active_clients.get(client_id)

    def add_chat_room(self, chat_room_name):
        def f():
            chat_room = self.get_chat_room_by_name(chat_room_name)
            if not chat_room:
                chat_room = ChatRoom(chat_room_name)
                chat_room_id = chat_room.id
                self.chat_rooms[chat_room_id] = chat_room
            return chat_room

        return safe(self.chat_rooms_lock, partial(f))

    def remove_chat_room(self, chat_room_id):
        chat_room = self.chat_rooms.pop(chat_room_id, None)
        if not chat_room:
            raise NonExistantChatRoomError(chat_room_id)

    def get_chat_room_by_name(self, chat_room_name):
        for chat_room_id in self.chat_rooms:
            chat_room = self.get_chat_room_by_id(chat_room_id)
            if chat_room.name == chat_room_name:
                return chat_room
        return None

    def get_chat_room_by_id(self, chat_room_id):
        return self.chat_rooms.get(int(chat_room_id))
