import socket
import sys
import random

class TestBot(object):

    def __init__(self):
        return

def main():
    if len(sys.argv) > 1:
        botId = "testbot" + str(sys.argv[1])
    tb = TestBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))
    s.send(botId)

if __name__ == "__main__":
    main()
