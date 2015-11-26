def isKillCommand(data):
    return data == "KILL_SERVICE\n"

def isHELOtext(data):
    return data[:4] == "HELO\n"

def formatDataToMessage(data, host, port, studentID):

    response = data;

    if isHELOtext(data):
        # Convert data to uppercase
        uppercaseResponse = response.upper()

        # Format message
        info = (
            "IP:{0}\n"
            "Port:{1}\n"
            "StudentID:{2}\n"
        )

        response = uppercaseResponse + info

        response = response.format(host, port, studentID)

    else:
        response = response + " - Processed!"

    return response
