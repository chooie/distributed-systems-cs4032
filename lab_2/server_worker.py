import sys
from my_utils import formatDataToMessage
from random import randint
from time import sleep

STUDENT_NUMBER = 1234567890

def serverWorker(host, port, serverThread):
    sleep(randint(0, 3))
    response = formatDataToMessage(
        serverThread.data, host, port, STUDENT_NUMBER
    )

    sys.stdout.write("Processed:\n{0}".format(serverThread.data))

    # Respond to client
    serverThread.request.sendall(response)
