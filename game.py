import socket
import sys
import random
import pickle
import itertools
from gamestate import *
from player import *
from deck import *
from action import *
from game import *
from deck import *

class Game(object):

    def __init__(self, server, numPlayers):
        self.server = server
        self.numPlayers = numPlayers
        self.deck = Deck()

        # create players
        self.players = []
        for order, name in enumerate(self.server.sockets.keys()):
            newPlayer = Player(name)
            self.players.append(newPlayer)
            drawCard(newPlayer)

        # set starting player
        self.it = itertools.cycle(self.players)
        self.currPlayer = self.it.next()
        self.currPlayer.isMyTurn = True
        return

    def gameOver(self):
        return len(self.state.deck) == 0 or \
            len([p for p in self.state.players if p.isAlive]) == 1:

    def drawCard(self, player):
        player.hand.append(self.deck.draw())
        return

    def nextTurn(self):
        self.currPlayer.isMyTurn = False
        nextPlayer = self.it.next()
        while not nextPlayer.isAlive:
            nextPlayer = self.it.next()
        nextPlayer.isMyTurn = True
        nextPlayer.isTargetable = True
        self.currPlayer = nextPlayer
        return
        
    
    def run(self):
        
        while not gameOver():
            # starting player draws a card
            drawCard(currPlayer)

            legalActions = generateActions(self.currPlayer)
            self.currAction = self.server.sendGame(self)
            if self.currAction in legalActions:
                executeAction(self.currAction)
            else:
                raise Exception('illegal action')

            nextTurn()
        return

        
