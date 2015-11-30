import sys;
import os;

def isKillCommand(data):
    return data == "KILL_SERVICE\n"

def killServer():
    sys.stdout.write("Kill Request!")
    os._exit(0)

def cleanUpServer(server):
    server.shutdown()
    server.server_close()
    sys.exit

def refuseConnection(thread):
    sys.stdout.write(refusalStr.format(thread.data))
    thread.request.send("Connection Refused\n")
    thread.request.close();
