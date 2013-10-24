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
    cardList = [PRINCESS, COUNTESS, KING] + \
               [PRINCE, HANDMAIDEN, BARON, PRIEST]*2 + [GUARD]*5
    cardDist = [PRINCESS, COUNTESS, KING] + \
               [PRINCE, HANDMAIDEN, BARON, PRIEST]*2 + [GUARD]*5
    cardNames = {8:"Princess", 7:"Countess", 6:"King", 5:"Prince", \
                 4:"Handmaiden", 3:"Baron", 2:"Priest", 1:"Guard"}
    cardFreq = {PRINCESS:1, COUNTESS:1, KING:1, PRINCE:2, HANDMAIDEN:2, \
                BARON:2, PRIEST:2, GUARD:5}

    def __init__(self, defaultCards=None):
        if isinstance(defaultCards, list):
            self.cards = defaultCards
        else:
            self.cards = Deck.cardList[:]
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
