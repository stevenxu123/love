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
        legalActions = state.legalActions
        print "~~~~~~~~~~~~~"
        print "LEGAL ACTIONS"
        print "~~~~~~~~~~~~~"
        return

def main():
    bot = HumanBot()
    bot.run()

if __name__== "__main__":
    main()
