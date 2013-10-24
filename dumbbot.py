import pickle
import sys
import socket
import time
from deck import *
from gamestate import *

class DumbBot(object):

    def __init__(self):
        # prompt for IP, port, name, delay
        if len(sys.argv) == 5:
            addr = sys.argv[1]
            port = int(sys.argv[2])
            self.name = sys.argv[3]
            self.delay = int(sys.argv[4])
        else:
            addr = raw_input("Enter hostname/IP address: ")
            port = int(raw_input("Enter port #: "))
            self.name = raw_input("Enter bot name: ")
            self.delay = int(raw_input("Enter delay (-1 for step-through): "))

        # set up socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((addr, port))

        # send name, get rounds
        s.send(self.name)
        self.numRounds = int(s.recv(1024))
        s.send(self.name + " is all set!")

        # set member variables
        self.s = s

    def update(self, state):
        return

    def wait(self, delay):
        if delay < 0:
            pause = raw_input("Enter: ")
        else:
            time.sleep(delay + 0.1)

    def move(self, state):
        return state.legalActions[0]

    def myPlayer(self, state):
        for player in state.players:
            if player.name == self.name:
                return player
        raise Exception("Bot player is missing from game")

    def myOpponents(self, state):
        return [p for p in state.players if p.name != self.name]

    def run(self):
        # play games
        for r in range(self.numRounds):
            state = pickle.loads(self.s.recv(1024))
            # print field and bot player's information
            state.printField()
            state.printPlayer(self.myPlayer(state))

            while not state.gameOver:
                # allow bot to update itself using new state
                self.update(state)
                # if I am currPlayer, send my move
                if state.currPlayer.name == self.name:
                    # wait for specified delay (if any)
                    self.wait(self.delay)
                    self.s.send(pickle.dumps(self.move(state),
                                             pickle.HIGHEST_PROTOCOL))

                # load next state
                state = pickle.loads(self.s.recv(1024))
                # print field and bot player's information
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

