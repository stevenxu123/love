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
        return self.__dict__ == other.__dict__

    def drawCard(self, deck):
        """ draw a card from deck and add to hand """
        self.hand.append(deck.draw())
        return

    def playCard(self, card):
        """ remove card from hand and add to discard
            !!will break if card not in hand """
        self.hand.remove(card)
        self.discard.append(card)
        return

    def loseGame(self):
        # ONLY set alive via loseGame
        self.alive = False
        self.targetable = False
        self.discard += self.hand
        del self.hand[:]
        return
