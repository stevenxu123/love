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
        
    def generateActions(self):
        #TODO: make this nice and clean
        hand = self.currPlayer.hand
        actions = [(c, self.currPlayer, None, None) for c in hand]
        targets = [p for p in self.state.players if p.isTargetable and p is not self.state.currPlayer]

        if Deck.PRINCESS in hand:
            actions.remove((Deck.Princess, self.currPlayer, None, None))
        if Deck.COUNTESS in hand:
            pass    
        if Deck.KING in hand:
            if Deck.COUNTESS in hand:
                actions.remove((Deck.KING, self.currPlayer, None, None))
            else:
                actions.append([(Deck.KING, self.currPlayer, t, None) for t in targets]) 
        if Deck.PRINCE in hand:
            if Deck.COUNTESS in hand:
                actions.remove((Deck.PRINCE, self.currPlayer, None, None))
            else:
                actions.append([(Deck.PRINCE, self.currPlayer, t, None) for t in targets])
                actions.remove((Deck.PRINCE, self.currPlayer, None, None))
                actions.append((Deck.PRINCE, self.currPlayer, self.currPlayer, None))
        if Deck.HANDMAIDEN in hand:
            actions.remove((Deck.HANDMAIDEN, self.currPlayer, None, None))
            actions.append((Deck.HANDMAIDEN, self.currPlayer, self.currPlayer, None))
        if Deck.BARON in hand:
            actions.append([(Deck.BARON, self.currPlayer, t, None) for t in targets])
        if Deck.PRIEST in hand:
            actions.append([(Deck.PRIEST, self.currPlayer, t, None) for t in targets])
        if Deck.GUARD in hand:
            actions.append([(Deck.GUARD, self.currPlayer, t, g) for t in targets for g in Deck.cardset if g != Deck.GUARD])
        return actions


    def executeAction(self, action):
        # assuming action is a 4-tuple
        card = action[0]
        actor = action[1]
        target = action[2]
        guess = action[3]
            
        if card == Deck.PRINCESS:
            raise Exception('cannot play princess')
        elif card == Deck.COUNTESS:      
            pass
        elif card == Deck.KING:       
            if target is not None:
                temp = actor.hand
                actor.hand = target.hand
                target.hand = temp
        elif card == Deck.PRINCE:    
            if Deck.PRINCESS in target.hand:
                target.lose()
                target.discard.append(target.hand)
            else:
                target.discard.append(target.hand)
                target.hand.append(self.state.deck.draw())
        elif card == Deck.HANDMAIDEN:   
            actor.isTargetable = False
        elif card == Deck.BARON: 
            if actor.hand > target.hand:
                target.lose()
                target.discard.append(target.hand)
            elif actor.hand < target.hand:
                actor.lose()
                actor.discard.append(actor.hand)
        elif card == Deck.PRIEST: 
            pass
        elif card == Deck.GUARD:
            if guess in target.hand:
                target.lose()
                target.discard.append(target.hand)
        else:
            raise Exception('invalid action')



def main():

    # initialize the GameServer object
    serv = GameServer()

    # prompt for player/round info
    numPlayers = input("Enter # of players: ")
    numRounds = input("Enter # of rounds: ")

    # setting up server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((socket.gethostname(), 8002))
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
