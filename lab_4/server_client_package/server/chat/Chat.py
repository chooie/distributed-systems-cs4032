from chat_room import ChatRoom

from threading import Lock
from functools import partial
from server_client_package.shared_lib.error import DuplicateClientError,\
    DuplicateChatRoomError, NonExistantChatRoomError
from server_client_package.server.server_core.server_utils import \
    TerminateRequestThread
from server_client_package.shared_lib.utils import safe


class Chat:
    def __init__(self):
        # { 'client_name': (chat_rooms[], thread_handle) }
        self.active_clients = {}
        # { 'chat_room_name': chat_room_obj }
        self.chat_rooms = {}
        self.active_clients_lock = Lock()
        self.chat_rooms_lock = Lock()

    def add_active_client(self, client_name, client_id, thread_handle):
        def f():
            # Check client isn't already in dict
            if self.active_clients.get(self, client_name):
                raise DuplicateClientError(client_name)

            # Add client
            self.active_clients[client_name] = ([], thread_handle)

        safe(self.active_clients_lock, partial(f))

    def remove_active_client(self, client_name, client_id):
        def f():
            # Remove from active_clients
            client = self.active_clients.pop(client_name)
            client_chat_rooms = client[0]
            # TODO: Figure out if I really need this
            client_thread_handle = client[1]

            # Loop through chat rooms and remove client
            for chat_room in client_chat_rooms:
                chat_room.remove_member(client_name, client_id)

            raise TerminateRequestThread()

        def g():
            safe(self.chat_rooms_lock, partial(f))

        safe(self.active_clients_lock, partial(g))

    def add_chat_room(self, chat_room_name):
        if self.chat_rooms.get(chat_room_name):
            raise DuplicateChatRoomError()
        chat_room = ChatRoom(chat_room_name)
        self.chat_rooms[chat_room_name] = chat_room

    def remove_chat_room(self, chat_room_name):
        chat_room = self.chat_rooms.pop(chat_room_name, None)
        if not chat_room:
            raise NonExistantChatRoomError()


