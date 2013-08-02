class Player:

    def __init__(self, name):
        self.name = name
        #TODO: remove isMyTurn
        # (no longer necessary because GameState stores currPlayer)
        # already removed in game.py
        self.isMyTurn = False
        self.isAlive = True
        self.isTargetable = True
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

    def playCard(self, card=self.hand[0]):
        """ remove card from hand and add to discard
            !!will break if card not in hand """
        self.hand.remove(card)
        self.discard.append(card)
        return

    def loseGame(self):
        # ONLY set isAlive via loseGame
        self.isAlive = False
        self.isTargetable = False
        self.discard += self.hand
        del self.hand[:]
        return
