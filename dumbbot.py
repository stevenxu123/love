import pickle
import sys
import socket
from deck import *
from gamestate import *

class DumbBot(object):

    def __init__(self):
        # prompt for IP, port, name
        if len(sys.argv) == 4:
            addr = sys.argv[1]
            port = int(sys.argv[2])
            name = sys.argv[3]
        else:
            addr = raw_input("Enter hostname/IP address: ")
            port = int(raw_input("Enter port #: "))
            name = raw_input("Enter bot name: ")

        # set up socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((addr, port))
        # send name, get rounds
        s.send(name)
        numRounds = int(s.recv(1024))
        s.send(name + " is all set!")
        # update member variables
        self.name = name
        self.s = s
        self.numRounds = numRounds
        return

    def move(self, state):
        pause = raw_input("enter: ")
        return state.legalActions[0]

    def myPlayer(self, state):
        for player in state.players:
            if player.name == self.name:
                return player
        raise Exception("Bot player is missing from game")

    def run(self):
        # play games
        for r in range(self.numRounds):
            state = pickle.loads(self.s.recv(1024))

            while not state.gameOver:
                # print field and bot player's information
                state.printField()
                state.printPlayer(self.myPlayer(state))
                # if I am currPlayer, send my move
                if state.currPlayer.name == self.name:
                    self.s.send(pickle.dumps(self.move(state),
                                             pickle.HIGHEST_PROTOCOL))
                # load next state
                state = pickle.loads(self.s.recv(1024))

            # print field and bot player's information at end of game
            state.printField()
            state.printPlayer(self.myPlayer(state))

        # close bot socket
        self.s.close()

        return

def main():
    bot = DumbBot()
    bot.run()


if __name__ == "__main__":
    main()


