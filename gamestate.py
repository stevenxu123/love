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
        print "#"*50
        cardsLeft = len(self.deck.cards)
        print "cards left in deck:", "[]"*cardsLeft, cardsLeft
        print self.actionSentence(self.currAction)
        print

        # print each player's discards and status information
        for player in self.players:
            if not player.alive:
                print "     ", player.name, " (x_x\")"
            elif player == self.currPlayer:
                print "[][] ", player.name, " <(._.<)"
            elif not player.targetable:
                print "[]   ", player.name, " \(._.)/ can't touch this"
            else:
                print "[]   ", player.name

            print "disc:", [Deck.cardNames[card] for card in player.discard]
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
            return "%s played %s and guessed %s's hand (for a %s)" % \
                    (actor.name, Deck.cardNames[card], target.name, \
                     Deck.cardNames[guess])
        elif target:
            return "%s played %s and %s" % \
                    (actor.name, Deck.cardNames[card],
                     self.effectString(card, target.name))
        else:
            return "%s played %s and nothing happened" % \
                    (actor.name, Deck.cardNames[card])

    def effectString(self, card, targetName):
        if card == Deck.KING:
            return "swapped hands with " + targetName
        elif card == Deck.PRINCE:
            return "forced %s to discard and draw a new card" % (targetName,)
        elif card == Deck.HANDMAIDEN:
            return "can't be targeted this round"
        elif card == Deck.BARON:
            return "challenged %s to a duel" % (targetName,)
        elif card == Deck.PRIEST:
            return "peeked at %s's hand" % (targetName,)
        else:
            return "made an illegal move"

    def printPlayer(self, player, gameOver=False):
        """Print human-readable list of attributes for this player"""
        print "-"*50
        if not player.alive:
            if not gameOver:
                print "your name:  ", player.name, "\t\tstatus: (x_x\")"
            else:
                print "your name:  ", player.name, "\t\tstatus: (T_T\")"
                print "You lost! You have brought dishonor upon yourself."
                print "\n", "G"*19, "GOOD GAME", "G"*20
            return
        elif gameOver:
            print "your name:  ", player.name, "\t\tstatus: \(^-^)/"
            print "YOU WON! YOU ARE THE VERY BEST THAT NO ONE EVER WAS!!"
            print "\n", "G"*19, "GOOD GAME", "G"*20
            return
        elif player == self.currPlayer:
            print "your name:  ", player.name, "\t\tstatus: <(._.<)"
        elif not player.targetable:
            print "your name:  ", player.name, "\t\tstatus: \(._.)/"
        else:
            print "your name:  ", player.name, "\t\tstatus: (-_- )"

        print "your hand:  ", [Deck.cardNames[card] for card in player.hand]
        if player.peekCard:
            print "peek card:  ", Deck.cardNames[player.peekCard]
