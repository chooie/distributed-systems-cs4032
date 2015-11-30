import sys
from random import randint
from time import sleep
import server_worker_utils as utils

STUDENT_NUMBER = 1234567890


def server_worker(host, port, server_thread, semaphore):
    sleep(randint(0, 3))

    message = server_thread.data

    sys.stdout.write(message)

    # TODO: pass real parameters
    response = utils.create_joined_chat_room_message("room", "id", 0)

    # Respond to client
    server_thread.request.sendall(response)

    # Release semaphore
    semaphore.release()
