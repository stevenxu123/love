import socket
import sys
import random
import pickle
import itertools
from player import *
from deck import *
from gamestate import *

class Game(object):

    def __init__(self, server, numPlayers):
        self.server = server
        self.numPlayers = numPlayers
        self.deck = Deck()

        # create players
        self.players = []
        for name in self.server.sockets.keys():
            newPlayer = Player(name)
            self.players.append(newPlayer)
            newPlayer.drawCard(self.deck)

        # set starting player
        self.it = itertools.cycle(self.players)
        self.currPlayer = self.it.next()
        self.currAction = None
        return

    def gameOver(self):
        return not self.deck.cards or \
            len([p for p in self.players if p.alive]) == 1

    def nextTurn(self):
        nextPlayer = self.it.next()
        # gameOver prevents all players being dead
        while not nextPlayer.alive:
            nextPlayer = self.it.next()
        nextPlayer.targetable = True
        self.currPlayer = nextPlayer
        return

    def generateActions(self, actor):
        actions = []
        hand = actor.hand

        if Deck.COUNTESS in hand:
            actions.append( (Deck.COUNTESS, actor, None, None) )
        else:
            if Deck.KING in hand:
                actions += self.allTargetActions(Deck.KING, actor)
            elif Deck.PRINCE in hand:
                actions += self.allTargetActions(Deck.PRINCE, actor)

        if Deck.HANDMAIDEN in hand:
            actions.append( (Deck.HANDMAIDEN, actor, actor, None) )
        if Deck.BARON in hand:
            actions += self.allTargetActions(Deck.BARON, actor)
        if Deck.PRIEST in hand:
            actions += self.allTargetActions(Deck.PRIEST, actor)

        if Deck.GUARD in hand:
            actions += self.allTargetActions(Deck.GUARD, actor)

        # if no actions available, you must use your card(s) to target None
        # note: if GUARD is used to target None, guess is irrelevant
        if not actions:
            return [(card, actor, None, None) \
                    for card in hand if card is not Deck.PRINCESS]
        else:
            return actions


    def allTargetActions(self, card, actor):
        targets = [p for p in self.players if p.targetable and p is not actor]

        if card == Deck.GUARD:
            return [(card, actor, target, guess) \
                    for target in targets \
                    for guess in range(Deck.PRIEST, Deck.PRINCESS+1)]

        actions = [(card, actor, target, None) for target in targets]
        if card == Deck.PRINCE:
            actions.append( (card, actor, actor, None) )

        return actions


    def executeAction(self, action):
        # assume action is legal
        card, actor, target, guess = action
        actor.playCard(card)

        if card == Deck.KING and target is not None:
            actor.hand, target.hand = target.hand, actor.hand

        # target is not None check unnecessary: PRINCE always has target
        elif card == Deck.PRINCE:
            if Deck.PRINCESS in target.hand:
                target.loseGame()
            else:
                # assumes target has 1 card in hand
                target.playCard()
                target.drawCard(self.deck)

        elif card == Deck.HANDMAIDEN:
            # target is actor, actor is target
            target.targetable = False

        elif card == Deck.BARON:
            if actor.hand[0] > target.hand[0]:
                target.loseGame()
            elif actor.hand < target.hand:
                actor.loseGame()

        elif card == Deck.PRIEST and target is not None:
            actor.peekCard = target.hand[0]

        elif card == Deck.GUARD and target is not None:
            if guess in target.hand:
                target.loseGame()

        return

    def run(self):
        while not self.gameOver():
            # starting player draws a card
            self.currPlayer.drawCard(self.deck)

            self.legalActions = self.generateActions(self.currPlayer)
            currState = GameState(self.deck, self.players, self.currPlayer, \
                                self.legalActions, self.currAction, False)
            self.currAction = self.server.sendState(currState)
            while self.currAction not in self.legalActions:
                self.currAction = self.server.sendState(currState)

            self.executeAction(self.currAction)

            self.nextTurn()
        
        # pass final state to players
        finalState = GameState(self.deck, self.players, None, \
                                [], self.currAction, True)
        self.server.sendState(finalState)
        return
