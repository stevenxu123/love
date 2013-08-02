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

    def __init__(self):
        self.cards = Deck.cardDist[:]
        random.shuffle(self.cards)
        self.lastCard = self.cards.pop()
        return

    def draw(self):
        if not self.cards:
            # proposal: return self.lastCard?
            # game should not be drawing after this
            print 'last card drawn' #debug
            return self.lastCard
#            if self.lastCard != 0:
#                last = self.lastCard
#                self.lastCard = 0
#                return last
#            else:
#                raise Exception('no cards left in deck to draw')
        else:
            return self.cards.pop()
