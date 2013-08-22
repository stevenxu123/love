from deck import *
from gamestate import *
from dumbbot import *

class HumanBot(DumbBot):

    def move(self, state):
        if not state.legalActions:
            raise Exception("The only winning move is not to play.")

        print "~"*50
        print "           (>._.)> YOUR MOVE <(._.<)"
        print "~"*50

        allTargets = {}
        for action in state.legalActions:
            (card, _, target, _) = action
            if card not in allTargets:
                allTargets[card] = []
            if target not in allTargets[card]:
                allTargets[card].append(target)

        confirm = "n"
        while confirm in ("n", "N", "no", "NO", "No", "Nein", "NEIN"):
            confirm, action = self.promptAction(state, allTargets)

        return action

    def promptAction(self, state, allTargets):
        # choose a card
        allCards = allTargets.keys()

        for i, card in enumerate(allCards):
            print "(%d): [%s]" % (i, Deck.cardNames[card])

        if len(allCards) == 1:
            raw_input("select a card to play:  ")
            myCard = allCards[0]
        else:
            myCard = allCards[prompt("select a card to play:  ", \
                                     range(len(allCards)))]
        print

        # choose a target
        myTargets = allTargets[myCard]
        if len(myTargets) == 1:
            myTarget = myTargets[0]
        else:
            for i, target in enumerate(myTargets):
                targetName = target.name
                if targetName == self.name:
                    targetName = "You"
                print "(%d): %s" % (i, targetName)

            targetChoice = prompt("choose a target: ", range(len(myTargets)))
            myTarget = myTargets[targetChoice]
            print

        # if GUARD, choose a card to guess
        if myCard == Deck.GUARD:
            guesses = range(Deck.PRINCESS, Deck.GUARD, -1)
            for guess in guesses:
                print "(%d): [%s]" % (guess, Deck.cardNames[guess])
            myGuess = prompt("pick a card to guess: ", guesses)
            print
        else:
            myGuess = None

        myAction = (myCard, state.currPlayer, myTarget, myGuess)
        print "you are about to play %s%s." % \
              (Deck.cardNames[myCard], self.myActionSentence(myAction))
        confirm = raw_input("continue? ")
        print

        if confirm in ("n", "N", "no", "NO", "No", "Nein", "NEIN"):
            print "%s?? Please make up your mind..." % confirm
            print "~"*50

        return (confirm, myAction)

    def myActionSentence(self, action):
        card, actor, target, guess = action

        if target is None:
            return ", targeting no one"

        elif card == Deck.KING:
            return " and swap hands with %s" % (target.name,)
        elif card == Deck.PRINCE:
            if target.name == self.name:
                return " and make yourself discard and redraw"
            else:
                return " and make %s discard and redraw" % (target.name,)
        elif card == Deck.HANDMAIDEN:
            return ", which gives you immunity until next turn"
        elif card == Deck.BARON:
            return " and engage battle with %s" % (target.name,)
        elif card == Deck.PRIEST:
            return " and peek at %s's hand" % (target.name,)
        elif card == Deck.GUARD:
            return " and guess if %s's card is a %s" % \
                   (target.name, Deck.cardNames[guess])

        raise Exception("Impossible! That action cannot be done")


def prompt(firstMessage, options, secondMessage=None):
    if secondMessage is None:
        secondMessage = firstMessage

    try:
        answer = int(raw_input(firstMessage))
    except ValueError:
        answer = None

    while answer is None or answer not in options:
        try:
            answer = int(raw_input(secondMessage))
        except ValueError:
            answer = None

    return answer


def main():
    bot = HumanBot()
    bot.run()

if __name__== "__main__":
    main()
