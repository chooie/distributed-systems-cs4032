import server_client_package.server.server_message.message_handler_utils as \
    utils
import logging

from time import sleep
from functools import partial
from server_client_package.shared_lib.error import MessageHandlerError
from server_client_package.server.server_core.server_utils import \
    TerminateRequestThread
from message import message_to_dict, get_message_dict_type


def message_handler(server_thread):
    sleep(1)
    message = server_thread.data
    try:
        values = message_to_dict(message)

        if not len(values) > 0:
            raise TerminateRequestThread

        join_chatroom_f = partial(utils.handle_join_chat_room, values,
                                  server_thread)
        leave_chatroom_f = partial(utils.handle_leave_chat_room, values,
                                   server_thread)
        disconnect_f = partial(utils.handle_disconnect, values, server_thread)
        chat_f = partial(utils.handle_chat, values, server_thread)

        handlers = {
            "JOIN_CHATROOM": join_chatroom_f,
            "LEAVE_CHATROOM": leave_chatroom_f,
            "DISCONNECT": disconnect_f,
            "CHAT": chat_f
        }

        message_type = get_message_dict_type(values)

        if message_type not in handlers:
            # Todo: Make more specific
            raise Exception

        handlers[message_type]()
    except TerminateRequestThread:
        raise TerminateRequestThread
    except Exception, e:
        logging.exception(e)
        raise MessageHandlerError(message)
