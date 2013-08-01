class GameState(object):

    def __init__(self):
        self.deck = None
        self.players = []
        self.currPlayer = None
        self.lastAction = None
        self.gameOver = False
        return
