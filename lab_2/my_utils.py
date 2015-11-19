def formatDataToMessage(data, host, port, studentID):
    if data == "KILL_SERVICE\n":
        print "Kill Request"
        exit(0)

    # Convert data to uppercase
    uppercaseData = data.upper()

    # Format message
    info = (
        "IP:{0}\n"
        "Port:{1}\n"
        "StudentID:{2}\n"
    )

    response = uppercaseData + info

    response = response.format(host, port, studentID)

    return response
