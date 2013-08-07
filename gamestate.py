from deck import *

class GameState(object):

    def __init__(self, deck, players, currPlayer, legalActions, currAction, gameOver):
        self.deck = deck
        self.players = players
        self.currPlayer = currPlayer
        self.legalActions = legalActions
        self.currAction = currAction
        self.gameOver = gameOver

    def __str__(self):
        return str(self.__dict__)

    def printField(self):
        """Print human-readable layout of public game information"""
        print "="*50

        # print what happened on the previous turn
        print self.actionSentence(self.currAction)
        print
        
        # print the number of cards remaining in the deck
        cardsLeft = len(self.deck.cards)
        print "cards left in deck:", "[]"*cardsLeft, cardsLeft
        print
        
        # print each player's name, status, and discards
        for player in self.players:
            if not player.alive:
                print "     ", player.name, "  (x_x\")"
            elif player == self.currPlayer:
                print "[][] ", player.name, " <(._.<)"
            elif not player.targetable:
                print "[]   ", player.name, " \(._.)/"
            else:
                print "[]   ", player.name
            discards = ""
            for card in player.discard:
                discards += "[" + Deck.cardNames[card] + "]"
            print "disc:", discards
            print
        return

    def actionSentence(self, action):
        if action is None:
            return ""
        card, actor, target, guess = action

        if target is not None:
            if card == Deck.KING:
                result = "swapped hands with %s" % (target.name,)
            elif card == Deck.PRINCE:
                if not target.alive:
                    subResult = "the Princess!"
                else:
                    subResult = "a %s then draw" % (Deck.cardNames[target.discard[-1]],)
                result = "made %s discard %s" % (target.name, subResult)
            elif card == Deck.HANDMAIDEN:
                result = "can't be targeted this round"
            elif card == Deck.BARON:
                if actor.alive and target.alive:
                    subResult = "\t...and neither side prevails"
                elif actor.alive:
                    subResult = "\t...%s loses the duel with a %s" % \
                                (target.name, Deck.cardNames[target.discard[-1]])
                elif target.alive:
                    subResult = "\t...%s loses the duel with a %s" % \
                                (actor.name, Deck.cardNames[actor.discard[-1]])           
                result = "challenged %s to a duel...\n%s" % (target.name, subResult)  
            elif card == Deck.PRIEST:
                result = "peeked at %s's hand" % (target.name,)
            elif card == Deck.GUARD:
                if not target.alive:
                    subResult = "\t...It's super effective!"
                else:
                    subResult = "\t...It's not very effective..."
                result = "guessed that %s has a %s...\n%s" % \
                    (target.name, Deck.cardNames[guess], subResult)
        else:
            result = "nothing happened"
        return "%s played %s and %s" % (actor.name, Deck.cardNames[card], result)

    def printPlayer(self, player ):
        """Print human-readable list of attributes for this player"""
        print "-"*50
        print "your name:  ", player.name
        if self.gameOver:
            if player.alive:
                print "your status: \(^-^)/"
                print "YOU WON! YOU ARE THE VERY BEST THAT NO ONE EVER WAS!!"
            else:
                print "your status:  (T_T\")"
                print "You lost! You have brought dishonor upon yourself."
            print "\n", "GG "*6, "GOOD GAME ", "GG "*7
            return
        elif not player.alive:
            print "your status:  (x_x\") RIP"
            return
        elif player == self.currPlayer:
            print "your status: <(._.<) it's your turn!"
        elif not player.targetable:
            print "your status: \(._.)/ can't touch this"
        else:
            print "your status:  (-_- ) ... ... ..."

        hand = ""
        for card in player.hand:
            hand += "[" + Deck.cardNames[card] + "]"
        print "your hand:  ", hand
        if player.peekCard:
            print "peek card:  ", Deck.cardNames[player.peekCard]
        print
