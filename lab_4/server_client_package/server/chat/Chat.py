from threading import Lock
from functools import partial
from server_client_package.shared_lib.error import DuplicateClientError
from server_client_package.shared_lib.utils import safe


class Chat:
    def __init__(self):
        self.active_clients = {}
        self.chat_rooms = []
        self.active_clients_lock = Lock()
        self.chat_rooms_lock = Lock()

    def add_active_client(self, client_name, client_id, thread_handle):
        def f():
            # Check client isn't already in dict
            if self.active_clients.get(self, client_name):
                raise DuplicateClientError(client_name)

            # Add client
            self.active_clients[client_name] = thread_handle

        safe(self.active_clients_lock, partial(f))

    def remove_active_client(self, client_name, client_id):
        self.active_clients_lock.acquire()
        self.chat_rooms_lock.acquire()

        def f():
            # Remove from active_clients and chat_rooms
            self.active_clients.pop(client_name)

            # Loop through chat rooms and remove client
            for chat_room in self.chat_rooms:
                chat_room.remove_member(client_name, client_id)

        def g():
            safe(self.chat_rooms_lock, partial(f))

        safe(self.active_clients_lock, partial(g))
