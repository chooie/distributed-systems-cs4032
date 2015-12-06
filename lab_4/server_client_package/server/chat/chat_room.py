from threading import Lock
from functools import partial
from server_client_package.shared_lib.error import DuplicateChatClientError
from server_client_package.shared_lib.utils import safe


class ChatRoom:
    def __init__(self, chat_room_name):
        self.lock = Lock()
        self.chat_room_name = chat_room_name

        # { "foo": thread_handle, "bar": thread_handle } -- values aren't used.
        self.members = {}

    def remove_member(self, client_name):
        def f():
            self.members.pop(client_name, None)

            message = "{0} left the room.\n".format(client_name)

            for member_name in self.members:
                self.members[member_name].request.sendall(message)

        safe(self.lock, partial(f))

    def add_member(self, client_name, client_id, thread_handle):
        def f():
            if self.members.get(client_name):
                raise DuplicateChatClientError()
            self.members[client_name] = thread_handle
        safe(self.lock, partial(f))

    def send_message_to_all_members(self, message):
        for member_name in self.members:
            self.members[member_name].request.sendall(message)
