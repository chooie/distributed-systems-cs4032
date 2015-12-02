import threading
import client_utils as utils

from functools import partial
from server_client_package.shared_lib.constants import HOST, PORT


def helo_scenario(ip, port):
    helo = partial(utils.create_helo_message)
    utils.execute_scenario(ip, port, helo)


def disconnect_scenario(ip, port):
    disconnect = partial(utils.create_disconnect_message, 'bill')
    utils.execute_scenario(ip, port, disconnect)


def join_chat_scenario(ip, port):
    join_chat = partial(utils.create_join_chat_room_message, 'cats', 'charlie')
    utils.execute_scenario(ip, port, join_chat)


def run():
    threads = []

    # HELO scenario
    t = threading.Thread(
            target=helo_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

    # Disconnect scenario
    t = threading.Thread(
            target=disconnect_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

    # Test join chat room
    t = threading.Thread(
            target=join_chat_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

if __name__ == "__main__":
    run()
