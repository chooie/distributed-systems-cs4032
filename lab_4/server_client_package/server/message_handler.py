from random import randint
from time import sleep
from functools import partial
import message_handler_utils as utils
from ..shared_lib.error import MessageHandlerError


def message_handler(server_thread):
    sleep(randint(0, 3))

    try:
        message = server_thread.data
        values = utils.message_to_dict(message)
        request = server_thread.request

        join_chatroom = partial(utils.handle_join_chat_room, values, request)
        leave_chatroom = partial(utils.handle_leave_chat_room, values, request)
        disconnect = partial(utils.handle_disconnect, values, request)
        chat = partial(utils.handle_chat, values, request)

        handlers = {
            "JOIN_CHATROOM": join_chatroom,
            "LEAVE_CHATROOM": leave_chatroom,
            "DISCONNECT": disconnect,
            "CHAT": chat
        }

        message_type = utils.get_message_dict_type(values)

        handlers[message_type]()
    except:
        raise MessageHandlerError("Error in Message Handler")