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
