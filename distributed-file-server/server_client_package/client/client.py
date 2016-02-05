import logging
import os
import sys
import threading

import client_utils as utils
from shared_lib.constants import STATIC_HOST, STATIC_PORT
from shared_lib.message import create_helo_message, create_some_dummy_message

script_dir = os.path.dirname(__file__)  # Absolute dir the script is in
log_path = os.path.join(script_dir, 'client-log.log')


def run():
    logging.basicConfig(filename=log_path, level=logging.INFO)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    threads = []

    # HELO scenario
    t = threading.Thread(
            target=utils.execute_scenario,
            args=(STATIC_HOST, STATIC_PORT, create_helo_message)
    )
    threads.append(t)
    t.start()

    t = threading.Thread(
            target=utils.execute_scenario,
            args=(STATIC_HOST, STATIC_PORT, create_some_dummy_message)
    )
    threads.append(t)
    t.start()

    t = threading.Thread(
            target=utils.file_scenario,
            args=(STATIC_HOST, STATIC_PORT, "lorem_ipsum_large.txt")
    )
    threads.append(t)
    t.start()


if __name__ == "__main__":
    run()
