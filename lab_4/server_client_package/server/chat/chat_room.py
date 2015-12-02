from server_client_package.shared_lib.error import DuplicateChatClientError
from threading import Lock


class ChatRoom:
    def __init__(self, chat_room_name):
        self.lock = Lock()
        self.chat_room_name = chat_room_name

        # { "foo": None, "bar": None } -- values aren't used.
        self.members = {}

    def remove_member(self, client_name, client_id):
        self.lock.acquire()
        # Don't care whether or not anything was returned
        self.members.pop(client_name, None)
        self.lock.release()

    def add_member(self, client_name, client_id):
        self.lock.acquire()

        if self.members.get(client_name):
            raise DuplicateChatClientError()

        self.members[client_name] = None
        self.lock.release()

