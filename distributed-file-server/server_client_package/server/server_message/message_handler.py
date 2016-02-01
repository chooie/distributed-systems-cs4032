import logging

from server.server_core.server_utils import TerminateRequestThread
from message import message_to_dict


def message_handler(server_thread):
    message = server_thread.data
    try:
        values = message_to_dict(message)

        if not len(values) > 0:
            raise TerminateRequestThread

        print values
    except TerminateRequestThread:
        raise TerminateRequestThread
    except Exception, e:
        logging.exception(e)
