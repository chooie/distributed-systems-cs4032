import sys
import log


def is_kill_command(data):
    return data == "KILL_SERVICE\n"


def kill_server():
    sys.stdout.write("Kill Request!")
    sys.exit()


def clean_up_server(server):
    sys.stdout.write("Server shutting down...")
    server.shutdown()
    server.server_close()
    sys.exit()


def refuse_connection(thread):
    log.refused(thread.data)
    thread.request.send("Connection Refused\n")
    thread.request.close()
