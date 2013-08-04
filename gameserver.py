import socket
import pickle
from game import *
from deck import *
from player import *

class GameServer(object):

    def __init__(self):
        self.sockets = {}
        return

    def sendState(self, state):
        pickledState = pickle.dumps(state)
        for player in state.players:
            self.sockets[player.name].send(pickledState)
        if not state.gameOver:
            return pickle.loads(self.sockets[state.currPlayer.name].recv(1024))
        else:
            return
        

def main():

    # initialize the GameServer object
    serv = GameServer()

    # prompt for player/round info
    numPlayers = input("Enter # of players: ")
    numRounds = input("Enter # of rounds: ")

    # setting up server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((socket.gethostname(), 8000))
    s.listen(5)

    # wait for player connections 
    for p in range(numPlayers):
        conn, addr = s.accept()
        name = conn.recv(1024)
        print name
        print serv.sockets
        while name in serv.sockets:
            conn.send("name already taken, try again")
            name = conn.recv(1024)
            print "new " + name
        serv.sockets[name] = conn
        conn.send(name)
        conn.send(str(numRounds))

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
