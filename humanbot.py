from deck import *
from gamestate import *
from dumbbot import *

class HumanBot(DumbBot):

    def move(self, state):
        return self.polishedMakeMove(state)

    def verboseMakeMove(self, state):
        print "~"*50
        print "LEGAL ACTIONS"
        print "~"*50

        if not state.legalActions:
            print "Something wrong here; how can you have no legal actions?"
            return None

        # print exhaustive list of actions
        for i, action in enumerate(state.legalActions):
            print "[%d]\t %s" % (i, state.actionString(action))

        print "~"*40
        # prompt human to select an action by entering a number
        actionIndex = input("Select action to make: ")
        while actionIndex not in range(len(state.legalActions)):
            actionIndex = input("Please enter a number to select an action: ")
        print "~"*40

        return state.legalActions[actionIndex]

    def polishedMakeMove(self, state):
        if not state.legalActions:
            raise Exception("The only winning move is not to play.")

        print "~"*50
        print "YOUR MOVE"
        print "~"*50

        allTargets = {}
        for action in state.legalActions:
            (card, _, target, _) = action
            if card not in allTargets:
                allTargets[card] = []
            if target not in allTargets[card]:
                allTargets[card].append(target)

        confirm = "n"
        while confirm in ("n", "N", "no", "NO", "No", "Nein"):
            confirm, action = self.promptAction(state, allTargets)
            print "confirm: ", confirm
            print "action:  ", action
        print "~"*50

        return action

    def promptAction(self, state, allTargets):
        # choose a card
        print "playable cards: " ,
        allCards = allTargets.keys()
        for i, card in enumerate(allCards):
            print "(%d): [%s]      " % (i, Deck.cardNames[card]) ,
        print
        myCard = allCards[prompt("select a card:  ", range(len(allCards)))]
        print

        myTargets = allTargets[myCard]
        if len(myTargets) > 1:
            print "targetable players:  " ,
            for i, target in enumerate(myTargets):
                targetName = target.name
                if targetName == self.name:
                    targetName = "You"
                print "(%d): %s      " % (i, targetName),
            print
            targetChoice = prompt("choose a target: ", range(len(myTargets)))
            myTarget = myTargets[targetChoice]
        else:
            myTarget = myTargets[0]

        if myCard == Deck.GUARD:
            guesses = range(Deck.PRINCESS, Deck.GUARD, -1)
            for guess in guesses:
                print "(%d): [%s]" % (guess, Deck.cardNames[guess])
            myGuess = prompt("pick a card to guess: ", guesses)
        else:
            myGuess = None

        myAction = (myCard, state.currPlayer, myTarget, myGuess)
        print "You are about to play %s%s" % \
              (Deck.cardNames[myCard], self.myActionSentence(myAction))
        confirm = raw_input("Continue? ")
        print

        if confirm == "n":
            print "No?? Please make up your mind..."
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
            return "which grants you immunity from other cards for one round"
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
    except TypeError:
        answer = None

    while answer is None or answer not in options:
        try:
            answer = int(raw_input(secondMessage))
        except TypeError:
            answer = None

    return answer


def main():
    bot = HumanBot()
    bot.run()

if __name__== "__main__":
    main()
