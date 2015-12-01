from random import randint
from time import sleep

import log
import server_worker_utils as utils


def server_worker(host, port, server_thread, semaphore):
    sleep(randint(0, 3))

    message = server_thread.data

    # TODO: parse message
    utils.process_message(message)

    log.processed(message)

    # TODO: pass real parameters
    response = utils.create_joined_chat_room_message("room", "id", 0)

    # Respond to client
    server_thread.request.sendall(response)

    # Release semaphore
    semaphore.release()
