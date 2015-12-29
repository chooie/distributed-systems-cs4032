import itertools


class Client:
    new_id = itertools.count().next

    def __init__(self, name, chat_rooms, thread_handle):
        self.name = name
        self.chat_rooms = chat_rooms
        self.thread_handle = thread_handle
        self.id = Client.new_id()
