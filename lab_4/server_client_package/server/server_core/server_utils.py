import sys
import server_client_package.server.log


def is_kill_command(data):
    return data == "KILL_SERVICE\n"


def kill_server():
    sys.stdout.write("Kill Request!")
    sys.exit()


def begins_with_helo_text(data):
    return data[:4] == "HELO"


def handle_helo_message(ip, port, student_id, server_thread):
    info = (
            "IP:{0}\n"
            "Port:{1}\n"
            "StudentID:{2}\n"
        ).format(ip, port, student_id)
    server_thread.request.sendall(server_thread.data + info)


def clean_up_server(server):
    sys.stdout.write("Server shutting down...")
    server.shutdown()
    server.server_close()
    sys.exit()


def refuse_connection(thread):
    server_client_package.server.log.refused(thread.data)
    thread.request.send("Connection Refused\n")
    thread.request.close()
