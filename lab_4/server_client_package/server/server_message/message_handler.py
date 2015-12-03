import logging
import server_client_package.server.server_message.message_handler_utils as \
    utils

from functools import partial
from server_client_package.shared_lib.error import MessageHandlerError
from server_client_package.server.server_core.server_utils import \
    TerminateRequestThread
from message import message_to_dict, get_message_dict_type


def message_handler(server_thread):
    message = server_thread.data
    try:
        values = message_to_dict(message)
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

        message_type = get_message_dict_type(values)

        handlers[message_type]()
    except TerminateRequestThread:
        raise TerminateRequestThread
    except Exception, e:
        logging.exception(e)
        raise MessageHandlerError(message)
