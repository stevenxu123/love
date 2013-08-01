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
        self.sockets = {}
        return

    def getConnections(self, sock, playnum):
        # wait for connections
        for n in range(playnum):
            conn, addr = sock.accept()
            name = conn.recv(1024)
            self.sockets[name] = conn
        return

    def newGame(self):
        # start a new game
        self.state = GameState()
        self.state.deck = Deck()
        for name in self.sockets.keys():
            newPlayer = Player(name)
            newPlayer.hand.append(self.state.deck.draw())
            self.state.players.append(newPlayer)
        self.currPlayer = self.state.players[0]
        self.currPlayer.isMyTurn = True
        return

    def generateActions(self):
        legalTargets = [p for p in self.state.players if p.isTargetable and p is not self.state.currentPlayer]
        actions = []
        hand = self.currentPlayer.hand
        
        if Deck.COUNTESS in hand:
            actions.append(Action(self.currentPlayer, None, Deck.COUNTESS, None))
        else:
            if Deck.KING in hand:
                for target in legalTargets:
                    actions.append(Action(actor, target, Deck.KING, None))
            elif Deck.PRINCE in hand:
                for target in (legalTargets + [self.state.currentPlayer]):
                    actions.append(Action(actor, target, Deck.PRINCE, None))
        if Deck.HANDMAIDEN in hand:
            actions.append(Action(self.currentPlayer, self.currentPlayer, Deck.HANDMAIDEN, None))
        if Deck.BARON in hand:
            for target in legalTargets:
                actions.append(Action(actor, target, Deck.BARON, None))
        if Deck.PRIEST in hand:
            for target in legalTargets:
                actions.append(Action(actor, target, Deck.PRIEST, None))
        if Deck.GUARD in hand:
            actions.append(Action(actor, target, Deck.GUARD, None))
        return actions


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
            pass
        elif card == Deck.GUARD:
            pass
        else:
            raise Exception('invalid action')
            
    def advanceTurn(self):
        # want the next player cyclically who is still alive
        for i, player in enumerate(self.state.players):
            if player.isMyTurn:
                player.isMyTurn = False
                while True:
                    nextPlayer = self.state.players[(i+1) % len(self.state.players)]
                    if nextPlayer.isAlive:
                        nextPlayer.isMyturn = True
                        nextPlayer.isTargetable = True
                        self.state.currPlayer = nextPlayer
                        break
                break
        return

    def isGameOver(self):
        if len(self.state.deck) == 0 or len([p for p in self.state.players if p.isAlive]) == 1:
            return True
        else:
            return False 

def main():

    # initialize the GameServer object
    serv = GameServer()

    # prompt for player/round info
    numPlayers = input("Enter # of players: ")
    numRounds = input("Enter # of rounds: ")

    # setting up server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8000))
    s.listen(4)

    # wait for player connections 
    serv.getConnections(s, int(numPlayers))

    for n in range(numRounds):
        # start new game
        serv.newGame(int(numPlayers))
        # enter game loop
        while not self.state.gameOver:
            # current player draws a card
            self.state.currPlayer.hand.append(self.state.deck.draw())
            # generate possible moves for current player
            legalActions = serv.generateActions()
            # send game state to all players
            
            # receive move from starting player
           
            # execute action on game state
            if action in legalActions:
                serv.executeAction()
            else:
                raise Exception('illegal action')
            # check if the game is over
            if serv.isGameOver():
                self.state.gameOver = True
            else:
                # rotate starting player
                serv.advanceTurn()
        # figure out winner
                        
    # calculate total scores/stats

    s.close()

if __name__ == "__main__":
    main()
