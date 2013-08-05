from deck import *
from gamestate import *
from dumbbot import *

class HumanBot(DumbBot):

    def __init__(self):
        return

    def makeMove(self, state):
        verboseMakeMove(state)
        return

    def verboseMakeMove(self, state):
        print "~"*40
        print "LEGAL ACTIONS"
        print "~"*40

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
            print "A curious game; the only winning move is not to play."
            return None
        print "~~~~~~~~~~~~~"
        print "LEGAL ACTIONS"
        print "~~~~~~~~~~~~~"

        actionCards = []
        for action in state.legalActions:
            (card, _, _, _) = action
            if card not in actionCards:
                actionCards.append(card)
        for i, actionCard in enumerate(actionCards):
            print "[%d]\t %s" % (i, Deck.cardNames[actionCard])
        actionCard = actionCards[prompt("Select a card to play: ", \
                                        range(len(actionCards)))]
        print "~"*40
        targets = []
        for action in state.legalActions:
            (card, _, target, _) = action
            if target is not None and card == actionCard:
                targets.append(target)
        for i, target in enumerate(targets):
            print "[%d]\t %s" % (i, target.name)

        if not targets:
            return (actionCard, state.currPlayer, None, None)

        target = targets[prompt("Choose a target: ", range(len(targets)))]

        if actionCard == Deck.GUARD:
            guesses = range(Deck.PRIEST, Deck.PRINCESS+1)
            for guess in guesses:
                print "[%d]\t %s" % (guess, Deck.cardNames[guess])
            guess = prompt("Guess: ", guesses)
        else:
            guess = None

        return (actionCard, state.currPlayer, target, guess)

    def prompt(firstMessage, options):
        answer = input(firstMessage)
        while answer not in options:
            answer = input(firstMessage)
        return answer

def main():
    bot = HumanBot()
    bot.run()

if __name__== "__main__":
    main()
