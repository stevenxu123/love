
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
        print "#"*40
        print "cards left in deck:", "[]"*len(self.deck.cards)
        print "last action played:", actionString(self.currAction)
        print actionSentence(self.currAction)
        print "#"*40
        print "="*40

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

            print "-"*40
            print "discard:", [Deck.cardNames[card] for card in player.discard]
            print "="*40
        return

    def actionString(self, action):
        card, actor, target, guess = action

        if guess is not None:
            return "([%s] %s >> %s, guess: %s)" % \
                    (Deck.cardNames[card], actor.name, target.name, \
                     Deck.cardNames[card])
        else:
            return "([%s] %s >> %s)" % \
                    (Deck.cardNames[card], actor.name, target.name)

    def actionSentence(self, action):
        if not action:
            return ""

        card, actor, target, guess = action
        if guess is not None:
            return "%s played a %s and guessed %s's hand (for a %s)" % \
                    (actor.name, Deck.cardNames[card], target.name, \
                     Deck.cardNames[guess])
        elif target is not None:
            return "%s played a %s and %s" % \
                    (actor.name, Deck.cardNames[card],
                     effectString(card, target.name))

    def effectString(self, card, targetName):
        if card == Deck.KING:
            return "swapped hands with", targetName
        elif card == Deck.PRINCE:
            return "forced %s to discard and draw a new card" % (targetName,)
        elif card == Deck.HANDMAIDEN:
            return "gave %s shroud for the next round" % (targetName,)
        elif card == Deck.BARON:
            return "challenged %s to a duel" % (targetName,)
        elif card == Deck.PRIEST:
            return "peeked at %s's hand" % (targetName,)
        else:
            return "made an illegal move"
