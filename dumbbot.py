import pickle
from socket import *
from deck import *
from gamestate import *

class DumbBot(object):

    def __init__(self):
        return

    def move(self, state):
        print "moving"
        pause = raw_input("enter: ")
        return state.legalActions[0]

def main():
    # initialize the bot
    bot = DumbBot()

    # prompt for IP, port, name
    addr = raw_input("Enter hostname/IP address: ")
    port = raw_input("Enter port #: ")
    name = raw_input("Enter bot name: ")

    # set up socket connection
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect((addr, int(port)))

    # register name with server
    s.send(name)
    mess = s.recv(1024)
    print mess
    while mess != name:
        name = raw_input("Bot name already taken. Enter another name: ")
        s.send(name)
        mess = s.recv(1024)

    # play games
    rounds = "1"
    for r in range(int(rounds)):
        state = pickle.loads(s.recv(1024))
        while not state.gameOver:
            state.printField()
            if state.currPlayer.name == name:
                state.currPlayer.printPlayerInfo()
                s.send(pickle.dumps(bot.move(state)))
            state = pickle.loads(s.recv(1024))

    s.close()


if __name__ == "__main__":
    main()


