import sys


def is_kill_command(data):
    return data == "KILL_SERVICE\n"


def kill_server():
    sys.stdout.write("Kill Request!")
    sys.exit()


def clean_up_server(server):
    server.shutdown()
    server.server_close()
    sys.exit()


def refuse_connection(thread):
    refusal_str = "Refused:\n{0}"

    if thread.data[-2:] != "\n":
        refusal_str += "\n"

    sys.stdout.write(refusal_str.format(thread.data))
    thread.request.send("Connection Refused\n")
    thread.request.close()
