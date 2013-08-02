import pickle
from socket import *
from deck import *
from gamestate import *

class DumbBot(object):

    def __init__(self):
        return

    def makeMove(self, state):
        return state.legalActions[0]

def main():
    # initialize the bot
    bot = DumbBot()

    # prompt for IP, port, name
    addr = raw_input("Enter hostname/IP address: ")
    port = input("Enter port #: ")
    name = raw_input("Enter bot name: ")

    # set up socket connection
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect((addr, port))
    print "connection established!"

    s.send(name)

    state = pickle.loads(s.recv(1024))
    while not state.gameOver:
        if state.currPlayer.name == name:
            s.send(pickle.dumps(bot.makeMove(state)))
        state = pickls.loads(s.recv(1024))

    s.close()
    

if __name__ == "__main__":
    main()


