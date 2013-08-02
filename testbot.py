import socket
import sys
import random
import pickle
import deck

class TestBot(object):

    def __init__(self):
        return

def main():
    if len(sys.argv) > 1:
        botId = "testbot" + str(sys.argv[1])
    tb = TestBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((socket.gethostname(), 8000))
    s.send(botId)
    print "name " + botId + " sent!"

    data = s.recv(1024)
    state = pickle.loads(data)
    s.send(pickle.dumps(state.legalActions[0]))
    s.close()


if __name__ == "__main__":
    main()
