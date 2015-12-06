import threading
import client_utils as utils

from functools import partial
from server_client_package.shared_lib.constants import HOST, PORT


def helo_scenario(ip, port):
    helo = partial(utils.create_helo_message)
    utils.execute_scenario(ip, port, helo)


def bad_message_scenario(ip, port):
    bad = partial(utils.create_bad_message)
    utils.execute_scenario(ip, port, bad)


def disconnect_scenario(ip, port):
    disconnect = partial(utils.create_disconnect_message, 'bill')
    utils.execute_scenario(ip, port, disconnect)


def join_chat_scenario(ip, port, chat_room_name, client_name):
    join_chat = partial(utils.create_join_chat_room_message, chat_room_name,
                        client_name)
    utils.execute_scenario(ip, port, join_chat)


def leave_chat_scenario(ip, port, chat_room_name, client_name):
    leave_chat = partial(utils.create_leave_chat_room_message, chat_room_name,
                         0, client_name)
    utils.execute_scenario(ip, port, leave_chat)


def run():
    threads = []

    # # HELO scenario
    # t = threading.Thread(
    #         target=helo_scenario,
    #         args=(HOST, PORT)
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Bad message scenario
    # t = threading.Thread(
    #     target=bad_message_scenario,
    #     args=(HOST, PORT)
    # )
    # threads.append(t)
    # t.start()
    #
    # # Disconnect scenario
    # t = threading.Thread(
    #         target=disconnect_scenario,
    #         args=(HOST, PORT)
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Test join chat room
    # t = threading.Thread(
    #         target=join_chat_scenario,
    #         args=(HOST, PORT, "cats", "charlie")
    #     )
    # threads.append(t)
    # t.start()
    #
    # # Test leave chat room
    # t = threading.Thread(
    #         target=leave_chat_scenario,
    #         args=(HOST, PORT, "cats", "charlie")
    #     )
    # threads.append(t)
    # t.start()

    # Bill scenario
    t = threading.Thread(
            target=utils.bill_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

    # Charlie scenario
    t = threading.Thread(
            target=utils.charlie_scenario,
            args=(HOST, PORT)
        )
    threads.append(t)
    t.start()

if __name__ == "__main__":
    run()
