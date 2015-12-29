import itertools

from threading import Lock
from functools import partial
from server_client_package.shared_lib.error import DuplicateChatClientError
from server_client_package.shared_lib.utils import safe


class ChatRoom:
    new_id = itertools.count().next

    def __init__(self, chat_room_name):
        self.lock = Lock()
        self.name = chat_room_name
        self.id = ChatRoom.new_id()
        # { client_id: client_obj }
        self.members = {}

    def remove_member(self, client):
        def f():
            message = "{0} has left this chatroom.\n".format(client.name)

            message = (
                "CHAT:{0}\n"
                "CLIENT_NAME:{1}\n"
                "MESSAGE:{2}\n"
            ).format(self.id, client.name, message)

            self.send_message_to_all_members(message)

            self.members.pop(client.id, None)

            client.remove_chat_room(self)

        safe(self.lock, partial(f))

    def add_member(self, client):
        def f():
            if self.members.get(client.id):
                raise DuplicateChatClientError()
            self.members[client.id] = client

            message = "{0} has joined this chatroom.\n".format(client.name)

            message = (
                "CHAT:{0}\n"
                "CLIENT_NAME:{1}\n"
                "MESSAGE:{2}\n"
            ).format(self.id, client.name, message)

            self.send_message_to_all_members(message)

            client.add_chat_room(self)

        safe(self.lock, partial(f))

    def get_member_by_id(self, member_id):
        return self.members.get(int(member_id))

    def get_member_by_name(self, name):
        for member_id in self.members:
            member = self.get_member_by_id(member_id)
            if member.name == name:
                return member
        return None

    def send_message_to_all_members(self, message):
        for member_id in self.members:
            self.members[member_id].thread_handle.request.sendall(message)
