import pickle
import sys
from socket import *
from game import *
from deck import *
from player import *

class GameServer(object):

    def __init__(self):
        self.sockets = {}
        return

    def sendState(self, state):
        for player in state.players:
            self.sockets[player.name].send(pickle.dumps(state))
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
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
    s.bind((gethostname(), 8000))
    s.listen(5)

    # wait for player connections
    for p in range(numPlayers):
        conn, addr = s.accept()
        name = conn.recv(1024)
        serv.sockets[name] = conn
        conn.send(str(numRounds))
        message = conn.recv(1024)
        print message

    # run games
    for r in range(numRounds):
        game = Game(serv, numPlayers)
        game.run()

    # close player sockets
    for v in serv.sockets.values():
        v.close()

    # close server socket
    s.close()

    return


if __name__ == "__main__":
    main()
