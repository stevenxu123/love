import random

class Deck(object):
    PRINCESS = 8
    COUNTESS = 7
    KING = 6
    PRINCE = 5
    HANDMAIDEN = 4
    BARON = 3
    PRIEST = 2
    GUARD = 1
    cardSet = range(GUARD, PRINCESS + 1)
    cardDist = [PRINCESS, COUNTESS, KING] + \
            [PRINCE, HANDMAIDEN, BARON, PRIEST]*2 + [GUARD]*5
    cardNames = {8:"Princess", 7:"Countess", 6:"King", 5:"Prince", \
                4:"Handmaiden", 3:"Baron", 2:"Priest", 1:"Guard"}

    def __init__(self):
        self.cards = Deck.cardDist[:]
        random.shuffle(self.cards)
        self.lastCard = self.cards.pop()
        return

    def draw(self):
        if not self.cards:
            # game should not be drawing after this
            print 'no more cards' #debug
            return self.lastCard
        else:
            return self.cards.pop()
