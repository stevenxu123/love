from deck import *

class Player:

    def __init__(self, name):
        self.name = name
        self.alive = True
        self.targetable = True
        self.hand = []
        self.discard = []
        self.peekCard = None
        return

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name

    def __str__(self):
        return str(self.__dict__)

    def drawCard(self, deck):
        """Draw a card from deck and add to hand"""
        self.hand.append(deck.draw())
        return

#    not sure if this would work...
#    def playCard(self, card=self.hand[0]):
    def playCard(self, card=0):
        """Remove card from hand and add to discard
           !!will break if card not in hand
        """
        if card in self.hand:
            self.hand.remove(card)
            self.discard.append(card)
        else:
            # no-argument call to function (card == 0)
            self.discard.append(self.hand.pop())
        return

    def loseGame(self):
        """Lose the game by setting alive=False, targetable=False,
           and dropping all card(s) in hand into discard
        """
        # ONLY set alive via loseGame
        self.alive = False
        self.targetable = False
        self.discard += self.hand
        del self.hand[:]
        return

    def printPlayerInfo(self):
        """Print human-readable list of attributes for this player"""
        print "#"*40
        print "your name:  ", self.name
        print "your status:", ("alive!" if self.alive else "dead")
#        if not self.alive:
#            return
        print "targetable: ", self.targetable
        print "your hand:  ", [Deck.cardNames[card] for card in self.hand]
        if self.peekCard:
            print "peek card:  ", Deck.cardNames[self.peekCard]
        print "#"*40
