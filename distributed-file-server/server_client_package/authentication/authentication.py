from server.server_core.request_handler import ThreadedTCPRequestHandler


class AuthenticationHandler(ThreadedTCPRequestHandler):
    def handle_message(self):
        print "I'm an authentication handler!"
