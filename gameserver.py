import pickle
import socket
import sys
from game import *
from deck import *
from player import *

class GameServer(object):

    def __init__(self):
        self.sockets = {}
        self.scores = {}
        return

    def sendState(self, state):
        for player in state.players:
            self.sockets[player.name].send(pickle.dumps(state, pickle.HIGHEST_PROTOCOL))
        if not state.gameOver:
            return pickle.loads(self.sockets[state.currPlayer.name].recv(1024))
        else:
            return


def main():

    # initialize the GameServer object
    serv = GameServer()

    # prompt for player/round info
    if len(sys.argv) == 3:
        numPlayers = int(sys.argv[1])
        numRounds = int(sys.argv[2])
    else:
        numPlayers = int(input("Enter # of players: "))
        numRounds = int(input("Enter # of rounds: "))

    # setting up server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((socket.gethostname(), 8000))
    s.listen(5)

    # wait for player connections
    for p in range(numPlayers):
        conn, addr = s.accept()
        name = conn.recv(1024)
        serv.sockets[name] = conn
        serv.scores[name] = 0
        conn.send(str(numRounds))
        message = conn.recv(1024)
        print message

    # run games
    for r in range(numRounds):
        game = Game(serv, numPlayers)
        winners = game.run()
        for w in winners:
            serv.scores[w.name] += 1

    # close player sockets
    for v in serv.sockets.values():
        v.close()

    # close server socket
    s.close()

    return


if __name__ == "__main__":
    main()
