class Player:

    def __init__(self, name):
        self.name = name
        self.isMyTurn = False
        self.isAlive = True
        self.isTargetable = True
        self.hand = []
        self.discard = []
        return
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
