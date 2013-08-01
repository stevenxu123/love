import random

class Deck(object):
    #cards = ('Princess', 'Countess', 'King', 'Prince',\
    #        'Handmaiden', 'Baron', 'Priest', 'Guard')
    #values = {'Princess':8, 'Countess':7, 'King':6, 'Prince':5,\
    #        'Handmaiden':4, 'Baron':3, 'Priest':2, 'Guard':1} 
    #initial = ['Princess', 'Countess', 'King', 'Prince', 'Prince',\
    #        'Handmaiden', 'Handmaiden', 'Baron', 'Baron', 'Priest',\
    #        'Priest', 'Guard', 'Guard', 'Guard', 'Guard', 'Guard']

    # cards are represented by their numeric values
    cards = [8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1, 1]

    def __init__(self):
        self.deck = Deck.cards[:]
        random.shuffle(self.deck)
        self.lastCard = self.deck.pop()
        return

    def draw(self):
        if self.deck == []:
            if self.lastCard > 0:
                last = self.lastCard
                self.lastCard = 0
                return last
            else:
                raise Exception('no cards left in deck to draw')
        else:
            return self.deck.pop()
