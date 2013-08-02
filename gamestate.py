
class GameState(object):

    def __init__(self, deck, players, currPlayer, legalActions, currAction):
        self.deck = deck
        self.players = players
        self.currPlayer = currPlayer
        self.legalActions = legalActions
        self.currAction = currAction
