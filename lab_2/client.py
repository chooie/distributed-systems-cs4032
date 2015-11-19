import sys
from random import randint
from time import sleep
import socket
import threading

BUFFER_SIZE = 1024;
HOST = "0.0.0.0"
PORT_NUMBER = 8080

NUMBER_OF_CLIENTS = 10

def worker(num, ip, port, message):
    sys.stdout.write("Worker: {0}\n".format(num))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(BUFFER_SIZE)
        sleep(randint(1, 5))
        sys.stdout.write(response + "\n")
    finally:
        sock.close()

if __name__ == "__main__":

    threads = []
    for i in range(5):
        message = "HELO text: {}\n".format(i)
        t = threading.Thread(
            target = worker,
            args = (i, HOST, PORT_NUMBER, message)
        )
        threads.append(t)
        t.start()
