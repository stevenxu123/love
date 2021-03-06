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
            # you may only play a KING or PRINCE with no COUNTESS in hand
            if Deck.KING in hand:
                actions += self.allTargetActions(Deck.KING, actor)
            if Deck.PRINCE in hand:
                actions += self.allTargetActions(Deck.PRINCE, actor)

        if Deck.HANDMAIDEN in hand:
            actions.append( (Deck.HANDMAIDEN, actor, actor, None) )

        # BARON, PRIEST, GUARD are all targeting cards
        for card in (Deck.BARON, Deck.PRIEST, Deck.GUARD):
            if card in hand:
                actions += self.allTargetActions(card, actor)

        # if no actions available, you must use your card(s) to target None
        # note: if GUARD is used to target None, guess is irrelevant
        if not actions:
            return [(card, actor, None, None) \
                    for card in hand if card != Deck.PRINCESS]
        else:
            return actions


    def allTargetActions(self, card, actor):
        """ get all target(ing) actions for targeting card 'card' """
        targets = [p for p in self.players if p.targetable and p != actor]

        if card == Deck.GUARD:
            return [(card, actor, target, guess) \
                    for target in targets \
                    for guess in range(Deck.PRIEST, Deck.PRINCESS+1)]

        actions = [(card, actor, target, None) for target in targets]
        if card == Deck.PRINCE:
            actions.append((card, actor, actor, None))

        return actions


    def executeAction(self, action):
        # assume action is legal
        card, actor, target, guess = action
        # make actor and target point to the right players in self.players
        actor = self.players[self.players.index(actor)]
        actor.playCard(card)

        if target is None:
            self.currAction = (card, actor, target, guess)
            return

        target = self.players[self.players.index(target)]

        if card == Deck.COUNTESS:
            pass
        elif card == Deck.KING:
            actor.hand, target.hand = target.hand, actor.hand
            actor.peekCard = target.hand[0]
            target.peekCard = actor.hand[0]
        # target is not None check unnecessary: PRINCE always has target
        elif card == Deck.PRINCE:
            if Deck.PRINCESS in target.hand:
                target.loseGame()
            else:
                # assumes target has 1 card in hand
                target.playCard()
                target.drawCard(self.deck)
        elif card == Deck.HANDMAIDEN:
            # should be true: target is actor
            target.targetable = False
        elif card == Deck.BARON:
            actor.peekCard = target.hand[0]
            target.peekCard = actor.hand[0]
            if actor.hand[0] > target.hand[0]:
                target.loseGame()
            elif actor.hand[0] < target.hand[0]:
                actor.loseGame()
            # else: (tie) both players still alive
        elif card == Deck.PRIEST:
            actor.peekCard = target.hand[0]
        elif card == Deck.GUARD:
            if guess in target.hand:
                target.loseGame()
        self.currAction = (card, actor, target, guess)
        return

    def run(self):
        while not self.gameOver():
            # starting player draws a card
            self.currPlayer.drawCard(self.deck)

            # generate legalActions and package into GameState 'currState'
            self.legalActions = self.generateActions(self.currPlayer)
            currState = GameState(self.deck, self.players, self.currPlayer, \
                                  self.legalActions, self.currAction, False)

            # retrieve currPlayer's selected currAction based on currState
            action = self.server.sendState(currState)
            while action not in self.legalActions:
                action = self.server.sendState(currState)

            # execute the selected action
            self.executeAction(action)

            # advance to the next turn
            self.nextTurn()


#        winner = None
#        maxCard = -1
#        maxDiscardLen = -1
#        while self.currPlayer is not winner:
#            if self.currPlayer.hand[0] > maxCard:
#                winner = self.currPlayer
#                maxCard = self.currPlayer.hand[0]
#                maxDiscardLen = len(self.currPlayer.discard)
#            elif self.currPlayer.hand[0] < maxCard:
#                self.currPlayer.loseGame()
#            # else: use tie-breaker rules
#            elif len(self.currPlayer.discard) > maxDiscard:
#                winner = self.currPlayer
#                maxCard = self.currPlayer.hand[0]
#                maxDiscardLen = len(self.currPlayer.discard)
#            elif len(self.currPlayer.discard) < maxDiscard:
#                self.currPlayer.loseGame()
#            self.nextTurn()

        maxCard = max(p.hand[0] for p in self.players if p.alive)
        winners = [p for p in self.players if p.alive and p.hand[0] == maxCard]
        maxDiscard = max(len(p.discard) for p in winners)
        winners = [p for p in winners if len(p.discard) == maxDiscard]
        for w in winners:
            w.win = True

        # pass final state to players
        finalState = GameState(self.deck, self.players, None, \
                               [], self.currAction, True)

        self.server.sendState(finalState)

        # return winners
        return winners
