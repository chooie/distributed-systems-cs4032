import sys
from random import randint
from time import sleep
import socket
import threading

BUFFER_SIZE = 1024;
HOST = "10.6.26.213"
PORT_NUMBER = 8080

NUMBER_OF_CLIENTS = 20

def worker(num, ip, port, message):
    sleep(randint(1, 5))
    sys.stdout.write("Worker: {0}\n".format(num))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sys.stdout.write(response + "\n")
    finally:
        sock.close()

if __name__ == "__main__":

    threads = []
    for i in range(NUMBER_OF_CLIENTS):
        if i % 2 == 0:
            message = "HELO text\n"
        else:
            message = "Some message: {0}".format(i)
        t = threading.Thread(
            target = worker,
            args = (i, HOST, PORT_NUMBER, message)
        )
        threads.append(t)
        t.start()

    # Send kill message after 10 secs
    # sleep(10)
    # t = threading.Thread(
    #         target = worker,
    #         args = (NUMBER_OF_CLIENTS, HOST, PORT_NUMBER, "KILL_SERVICE\n")
    # )
    # t.start()
    # threads.append(t)
