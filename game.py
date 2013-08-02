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





    def generateActions(self, actor):
        actions = []
        hand = actor.hand

        if Deck.COUNTESS in hand:
            actions.append( (actor, None, Deck.COUNTESS) )
        else:
            if Deck.KING in hand:
                actions += allTargetActions(actor, Deck.KING)
            elif Deck.PRINCE in hand
                actions += allTargetActions(actor, Deck.PRINCE)

        if Deck.HANDMAIDEN in hand:
            actions.append( (actor, actor, Deck.HANDMAIDEN) )
        if Deck.BARON in hand:
            actions += allTargetActions(actor, Deck.BARON)
        if Deck.PRIEST in hand:
            actions += allTargetActions(actor, Deck.PRIEST)

        if Deck.GUARD in hand:
            actions += allTargetActions(actor, Deck.GUARD)

        # If no actions available, but have a targeting card in hand
        targetingCards = [Deck.KING, Deck.PRINCE, Deck.BARON, Deck.PRIEST, Deck.GUARD]
        hasTargetingCard = [card for card in Deck.cardSet if card in targetingCards]

        if len(actions) == 0:
            if hand[0] == Deck.PRINCESS:
                return allTargetActions(actor, hand[1])
            else:
                return allTargetActions(actor, hand[0])

        return actions


    def allTargetActions(self, actor, card):
        targets = [p for p in self.players if p.isTargetable and p is not actor]

        if card == Deck.GUARD:
            return [(actor, target, card, guess) \
                    for target in targets for guess in range(Deck.PRIEST, Deck.PRINCESS+1)]

        actions = [(actor, target, card) for target in targets]
        if card == Deck.PRINCE:
            actions.append( (actor, actor, card) )

        return actions


    def run(self):

        while not gameOver():
            # starting player draws a card
            drawCard(currPlayer)

            self.legalActions = generateActions(self.currPlayer)
            self.currAction = self.server.sendGame(self)
            while self.currAction not in self.legalActions:
                self.currAction = self.server.sendGame(self)

            executeAction(self.currAction)

            nextTurn()
        return


