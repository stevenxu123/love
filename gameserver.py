import socket
import pickle
from game import *
from deck import *
from player import *

class GameServer(object):

    def __init__(self):
        self.sockets = {}
        return

    def getConnections(self, sock, numPlayers):
        for n in range(numPlayers):
            conn, addr = sock.accept()
            name = conn.recv(1024)
            self.sockets[name] = conn
        return

    def sendGame(self, game):
        pickledGame = pickle.dumps(game)
        for player in game.players:
            self.sockets[player.name].send(pickledGame)
        return pickle.loads(self.sockets[game.currPlayer.name].recv(1024))
        

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
    s.listen(4)

    # wait for player connections 
    serv.getConnections(s, int(numPlayers))
    print "connection received!"

    for n in range(numRounds):
        game = Game(serv, numPlayers)
        game.run()
    
    # close player sockets
    for k,v in serv.sockets():
        v.close()

    # close server socket
    s.close()

    return


if __name__ == "__main__":
    main()
