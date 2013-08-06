import pickle
import sys
import socket
from deck import *
from gamestate import *

class DumbBot(object):

    def __init__(self):
        return

    def move(self, state):
        pause = raw_input("enter: ")
        return state.legalActions[0]

def main():

    # initialize the bot
    bot = DumbBot()

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

    # play games
    for r in range(numRounds):
        state = pickle.loads(s.recv(1024))
        while not state.gameOver:
            state.printField()
            # print bot's player's information
            for player in state.players:
                if player.name == name:
                    state.printPlayer(player)
                    break

            if state.currPlayer.name == name:
                s.send(pickle.dumps(bot.move(state), pickle.HIGHEST_PROTOCOL))

            state = pickle.loads(s.recv(1024))

        state.printField()
        for player in state.players:
            if player.name == name:
                state.printPlayer(player, gameOver=True)
                break


    # close bot socket
    s.close()

    return


if __name__ == "__main__":
    main()


