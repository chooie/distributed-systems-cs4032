import sys
from random import randint
from time import sleep

STUDENT_NUMBER = 1234567890

def serverWorker(host, port, serverThread, semaphore):
    sleep(randint(0, 3))


    response = "Message Received.\n"

    # Respond to client
    serverThread.request.sendall(response)

    # Release semaphore
    semaphore.release()
