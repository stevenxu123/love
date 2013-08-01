class GameState(object):

    def __init__(self):
        self.deck = None
        self.players = []
        self.alivePlayers = 0
        self.currentPlayer = None
        self.lastAction = None
        self.gameOver = False
        return
