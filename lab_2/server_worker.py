from my_utils import formatDataToMessage

STUDENT_NUMBER = 1234567890

def serverWorker(host, port, serverThread):
    response = formatDataToMessage(
        serverThread.data, host, port, STUDENT_NUMBER
    )

    # Respond to client
    serverThread.request.sendall(response)
