import socket
import sys
import random
import pickle
from gamestate import *
from player import *
from deck import *
from action import *

class GameServer(object):

    def __init__(self):
        self.state = GameState()
        self.sockets = {}
        return

    def getConnections(self, sock, playnum):
        # get connections and create all Players
        for i in range(playnum):
            conn, addr = sock.accept()
            name = conn.recv(1024)
            self.sockets[name] = conn
            self.state.players.append(Player(name))
        return

    def startGame(self):
        # generate the initial state of the game
        self.state.deck = Deck()
        for player in self.state.players:
            player.hand = [self.state.deck.draw()]
        self.currentPlayer = self.state.players[0]
        self.currentPlayer.isMyTurn = True
        return

    def generateMoves(self):
        #iterate through both cards in hand
        #for each card, create tuples of (card name, target, guess)
        #can't target handmaidens
        #guess is only for guard
        legalTargets
        moves = []
        for card in self.hands[self.startingPlayer]:
            if card == 'Guard':
                for 

    def executeAction(self, action):

        card = action.card
        actor = action.actor
        target = action.target
        guess = action.guess
            
        if card == Deck.PRINCESS:
            raise Exception('cannot play princess')
        elif card == Deck.COUNTESS:      
            pass
        elif card == Deck.KING:       
            if target != None:
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
        elif card == Deck.GUARD:
        else:
            raise Exception('invalid action')
            

        
                


def main():

    # initialize server
    gs = GameServer()

    # prompt for player/round info
    numPlayers = input("Enter # of players: ")
    numRounds = input("Enter # of rounds: ")

    # setting up server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8000))
    s.listen(4)

    # wait for player connections 
    gs.getConnections(s, int(numPlayers))

    # initialize game state
    gs.startGame()

    #pickle.dump(gs, open('blah.p', 'wb'))
    #s.send(
    for n in range(numRounds):
        # enter game loop
        while not self.state.gameOver:
            #starting player draw a card
            self.state.currentPlayer.hand.append(self.state.deck.draw())
            #generate possible moves for starting player
            gs.generateActions()
            #send game state to all players
            
            #receive move from starting player
            
            #execute action on game state
            if action in legalActions:
                gs.executeAction()
            #check if game is over
            if len(self.state.deck) == 0 or self.state.alivePlayers == 1
                self.state.gameOver = True
            else:
            #rotate starting player
                if self.state.players[-1].isMyTurn:
                    self.state.players[-1].isMyTurn = False
                    self.state.players[0].isMyTurn = True
                    self.state.currentPlayer = self.state.players[0]
                else:
                    for player in self.state.players:
                        if 
        # figure out winner

                
    # calculate total scores/stats

    s.close()

if __name__ == "__main__":
    main()
