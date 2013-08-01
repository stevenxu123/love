class Player:

    def __init__(self, name):
        self.name = name
        self.isMyTurn = False
        self.isAlive = True
        self.isTargetable = True
        self.hand = []
        self.discard = []
        return
