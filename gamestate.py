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
        """Print field: public game information known to all players"""
        print "="*50
        cardsLeft = len(self.deck.cards)
        print "cards left in deck:", "[]"*cardsLeft, cardsLeft

        # print what happened on the previous turn
        print self.actionSentence(self.currAction)
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

    def actionString(self, action):
        if action is None:
            return ""

        card, actor, target, guess = action

        if guess is not None:
            return "([%s] %s >> %s, guess: %s)" % \
                    (Deck.cardNames[card], actor.name, target.name, \
                     Deck.cardNames[card])
        elif target is not None:
            return "([%s] %s >> %s)" % \
                    (Deck.cardNames[card], actor.name, target.name)
        else:
            return "([%s] %s >> %s)" % \
                    (Deck.cardNames[card], actor.name, None)

    def actionSentence(self, action):
        if action is None:
            return ""

        card, actor, target, guess = action
        if guess:
            if not target.alive:
                return "%s played %s and guessed %s's hand correctly (for a %s)" % \
                    (actor.name, Deck.cardNames[card], target.name, \
                     Deck.cardNames[guess])
            else:
                return "%s played %s and guessed %s's hand (for a %s)" % \
                    (actor.name, Deck.cardNames[card], target.name, \
                     Deck.cardNames[guess])
        elif target:
            return "%s played %s and %s" % \
                    (actor.name, Deck.cardNames[card],
                     self.effectString(card, actor, target))
        else:
            return "%s played %s and nothing happened" % \
                    (actor.name, Deck.cardNames[card])

    def effectString(self, card, actor, target):
        if card == Deck.KING:
            return "swapped hands with " + target.name
        elif card == Deck.PRINCE:
            if not target.alive:
                return "forced %s to discard the Princess!" % (target.name,)
            else:
                return "forced %s to discard a %s and draw a new card" % \
                        (target.name, Deck.cardNames[target.discard[-1]])
        elif card == Deck.HANDMAIDEN:
            return "can't be targeted this round"
        elif card == Deck.BARON:
            if target is None:
                result = ""
            elif actor.alive and target.alive:
                result = "and the duel ends in a tie"
            elif actor.alive:
                result = "%s loses the duel (with a %s)" % \
                        (target.name, Deck.cardNames[target.discard[-1]])
            else:
                result = "%s loses the duel (with a %s)" % \
                        (actor.name, Deck.cardNames[actor.discard[-1]])           
            return "challenged %s to a duel\n" % (target.name,) + result
        elif card == Deck.PRIEST:
            return "peeked at %s's hand" % (target.name,)
        else:
            return "made an illegal move"

    def printPlayer(self, player, gameOver=False):
        """Print human-readable list of attributes for this player"""
        print "-"*50
        print "your name:  ", player.name
        if not player.alive:
            if not gameOver:
                print "your status:  (x_x\")"
            else:
                print "your status:  (T_T\")"
                print "You lost! You have brought dishonor upon yourself."
                print "\n", "GG "*6, "GOOD GAME ", "GG "*7
            return
        elif gameOver:
            print "your status: \(^-^)/"
            print "YOU WON! YOU ARE THE VERY BEST THAT NO ONE EVER WAS!!"
            print "\n", "GG "*6, "GOOD GAME ", "GG "*7
            return
        elif player == self.currPlayer:
            print "your status: <(._.<) it's your turn!"
        elif not player.targetable:
            print "your status: \(._.)/ can't touch this"
        else:
            print "your status:  (-_- )"

        print "your hand:  ", [Deck.cardNames[card] for card in player.hand]
        if player.peekCard:
            print "peek card:  ", Deck.cardNames[player.peekCard]
