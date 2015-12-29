import itertools


class Client:
    new_id = itertools.count().next

    def __init__(self, name, thread_handle):
        self.name = name
        # { chat_room_id: chat_room_obj}
        self.chat_rooms = {}
        self.thread_handle = thread_handle
        self.id = Client.new_id()

    def add_chat_room(self, chat_room):
        self.chat_rooms[chat_room.id] = chat_room

    def remove_chat_room(self, chat_room):
        self.chat_rooms.pop(chat_room.id)
