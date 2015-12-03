from threading import Lock
from functools import partial
from server_client_package.shared_lib.error import DuplicateChatClientError
from server_client_package.shared_lib.utils import safe


class ChatRoom:
    def __init__(self, chat_room_name):
        self.lock = Lock()
        self.chat_room_name = chat_room_name

        # { "foo": None, "bar": None } -- values aren't used.
        self.members = {}

    def remove_member(self, client_name, client_id):
        def f():
            self.members.pop(client_name, None)

        safe(self.lock, partial(f))

    def add_member(self, client_name, client_id):
        def f():
            if self.members.get(client_name):
                raise DuplicateChatClientError()
            self.members[client_name] = None
        safe(self.lock, partial(f))
