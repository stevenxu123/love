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
            self.drawCard(newPlayer)

        # set starting player
        self.it = itertools.cycle(self.players)
        self.currPlayer = self.it.next()
        self.currPlayer.isMyTurn = True
        self.currAction = None
        return

    def gameOver(self):
        return len(self.deck.cards) == 0 or \
            len([p for p in self.players if p.isAlive]) == 1

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
        #TODO change the action tuple order to (card, actor, target, guess)
        # also change it for executeActions
        actions = []
        hand = actor.hand

        if Deck.COUNTESS in hand:
            actions.append((actor, None, Deck.COUNTESS))
        else:
            if Deck.KING in hand:
                actions += self.allTargetActions(actor, Deck.KING)
            elif Deck.PRINCE in hand:
                actions += self.allTargetActions(actor, Deck.PRINCE)

        if Deck.HANDMAIDEN in hand:
            actions.append((actor, actor, Deck.HANDMAIDEN))
        if Deck.BARON in hand:
            actions += self.allTargetActions(actor, Deck.BARON)
        if Deck.PRIEST in hand:
            actions += self.allTargetActions(actor, Deck.PRIEST)

        if Deck.GUARD in hand:
            actions += self.allTargetActions(actor, Deck.GUARD)

        # If no actions available, but have a targeting card in hand
        targetingCards = [Deck.KING, Deck.PRINCE, Deck.BARON, Deck.PRIEST, Deck.GUARD]
        hasTargetingCard = [card for card in Deck.cardSet if card in targetingCards]

        if len(actions) == 0:
            if hand[0] == Deck.PRINCESS:
                return self.allTargetActions(actor, hand[1])
            else:
                return self.allTargetActions(actor, hand[0])

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

    def executeAction(self, action):
        # assuming action is a 4-tuple
        # TODO really need to rewrite this
        actor = action[0]
        target = action[1]
        card = action[2]
        if len(action) > 3:
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
                #target.lose()
                target.discard.append(target.hand)
            else:
                target.discard.append(target.hand)
                target.hand.append(self.deck.draw())
        elif card == Deck.HANDMAIDEN:   
            actor.isTargetable = False
        elif card == Deck.BARON: 
            if actor.hand > target.hand:
                #target.lose()
                target.discard.append(target.hand)
            elif actor.hand < target.hand:
                #actor.lose()
                actor.discard.append(actor.hand)
        elif card == Deck.PRIEST: 
            pass
        elif card == Deck.GUARD:
            if guess in target.hand:
                #target.lose()
                target.discard.append(target.hand)
        else:
            raise Exception('invalid action')

        return

    def run(self):
        while not self.gameOver():
            # starting player draws a card
            self.drawCard(self.currPlayer)

            self.legalActions = self.generateActions(self.currPlayer)
            print self.legalActions
            currState = GameState(self.deck, self.players, \
                        self.currPlayer, self.legalActions, self.currAction)
            self.currAction = self.server.sendGame(currState)
            print self.currAction
            print self.currAction in self.legalActions
            while self.currAction not in self.legalActions:
                self.currAction = self.server.sendGame(currState)

            self.executeAction(self.currAction)

            self.nextTurn()
        return
