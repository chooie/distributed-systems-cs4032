from server.server_core.request_handler import ThreadedTCPRequestHandler


class DirectoryHandler(ThreadedTCPRequestHandler):
    def handle_message(self):
        print "I'm a file directory handler!"
