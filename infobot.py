from deck import *
from dumbbot import *

class InfoBot(DumbBot):

    def __init__(self, trackCards=True):
        DumbBot.__init__(self)
        self.trackCards = trackCards

    def update(self, state):
        """Update logic needed to deduce other players' cards

        Covers all scenarios except the following:
          - advanced sudoku process-of-elimination logic
              > 2 players each hold either card A or card B, and there is
                only 1 copy of each card (A and B) left in the deck.
                Remaining players logically cannot hold card A or card B
          - advanced BARON tie logic
              > 2 players who previously tied with BARON hold unknown cards.
                1 player PRINCEs self, revealing their entire hand. The other
                player must be holding either a PRINCE or the discarded card.

        DOES cover the simpler cases:
          - easy process-of-elimination
              > 1 player is known to hold card A. Remaining players cannot
                hold card A if there are no other copies left in the deck.
          - normal BARON tie logic
              > 2 players who previously tied with BARON hold unknown cards.
                1 player reveals he does not have card A, so the other
                player cannot possibly have card A. Alternatively, player 1's
                card is revealed to be card B. Player 2's card must be card B.

        """
        if not self.trackCards:
            return
        # update self.unseenCards (cards that are not visible to myPlayer)
        # unseenCards does not consider peekCards and deduced cards
        self.player = self.myPlayer(state)
        self.unseenCards = Deck.cardFreq.copy()
        seenCards = [card for p in state.players for card in p.discard]
        seenCards += self.player.hand
        for card in seenCards:
            self.unseenCards[card] -= 1

        ############################################################
        # variable initialization for beginning of new game
        if state.currAction is None:
            self.suspectCards = {}
            self.peekCards = {}
            self.antiCards = {}
            self.tied = {}
            self.leakCard = None
            for p in state.players:
                self.suspectCards[p.name] = self.unseenCards
                self.peekCards[p.name] = None
                self.antiCards[p.name] = set()
                self.tied[p.name] = None
            self.printSuspectCards(state, self.suspectCards)
            return
        ############################################################
        # else not beginning of new game...

        (card, actor, target, guess) = state.currAction

        # NOTE: neither resetLogic nor updateLogic assume any info about
        #       unseenCards; if they did they would need to go in the loop
        #
        # reset info (trash previous deductions for actor if necessary)
        self.resetLogic(card, actor)
        # more info to deduce if last player (actor) targeted someone
        if target is not None:
            self.updateLogic(card, actor, target, guess)

        # repeatedly deduce suspectCards until we reach logical equilibrium
        #   - in one iteration, if one person's hand becomes fully deduced,
        #     that affects the suspectCards in everyone else's hands
        equilibrium = False
        while not equilibrium:
            equilibrium = self.deduce(state,
                                      self.unseenCards,
                                      self.suspectCards)

        self.printSuspectCards(state, self.suspectCards)

    def resetLogic(self, card, actor):
        # if I played a leakCard, then my hand is now unknown to others
        if actor == self.player and card == self.leakCard:
            self.leakCard = None

        # peek information no longer valid once player plays known card
        elif card == self.peekCards[actor.name]:
            self.peekCards[actor.name] = None

        # deduced info no longer holds once player plays a non-antiCard
        elif card not in self.antiCards[actor.name]:
            self.antiCards[actor.name].clear()
            # unsync players with identical hands (who tied)
            twin = self.tied[actor.name]
            if twin is not None:
                self.tied[twin.name] = None
                self.tied[actor.name] = None
                # missing logic for if both of actor's cards are revealed,
                # which limits twin's hand to 2 possibilities (or fewer)
                # (i.e. actor PRINCEs self, or KINGs me)
                #
                # logic for one-sided ties (only 1 tied card may be hidden)
                # is super complicated, BUT since ties are uncommon,
                # sub-optimal logic here might be ok

    def updateLogic(self, card, actor, target, guess):

        if card == Deck.KING:
            # if I was involved in the KING play (as actor or target)
            # then I have full information; no need to determine antiCards
            if target == self.player:
                self.peekCards[actor.name] = self.player.peekCard
                self.leakCard = actor.peekCard
            elif actor == self.player:
                self.peekCards[target.name] = self.player.peekCard
                self.leakCard = target.peekCard
            # else information may be incomplete; update antiCards
            else:
                self.antiCards[actor.name].add(Deck.COUNTESS)
                swap = self.antiCards[actor.name]
                self.antiCards[actor.name] = self.antiCards[target.name]
                self.antiCards[target.name] = swap
                swap = self.peekCards[actor.name]
                self.peekCards[actor.name] = self.peekCards[target.name]
                self.peekCards[target.name] = swap

        elif card == Deck.PRINCE:
            self.antiCards[actor.name].add(Deck.COUNTESS)
            self.peekCards[target.name] = None
            self.antiCards[target.name].clear()

        # BARON logic is redonkulous
        elif card == Deck.BARON:
            if actor.alive and target.alive:
                # if there is a tie...
                # if my player was the actor or target
                if self.player == target or self.player == actor:
                    # update leakCard, peek at my own hand
                    # hand[0] is always card before drawing if I am currPlayer
                    self.leakCard = self.player.hand[0]
                    self.peekCards[self.name] = self.player.hand[0]
                # update peekCard owners
                if self.peekCards[actor.name] is not None:
                    self.peekCards[target.name] = self.peekCards[actor.name]
                elif self.peekCards[target.name] is not None:
                    self.peekCards[actor.name] = self.peekCards[target.name]

                # the next two cases should basically never show up
                elif self.tied[actor.name] not in (None, target):
                    print "warning, two players just BARONed with GUARD"
                    print "in the same round!"
                    twin = self.tied[actor.name]
                    self.peekCards[actor.name] = Deck.GUARD
                    self.peekCards[target.name] = Deck.GUARD
                    self.peekCards[twin.name] = Deck.GUARD
                elif self.tied[target.name] not in (None, actor):
                    print "warning, two players just BARONed with GUARD"
                    print "in the same round!"
                    twin = self.tied[target.name]
                    self.peekCards[actor.name] = Deck.GUARD
                    self.peekCards[target.name] = Deck.GUARD
                    self.peekCards[twin.name] = Deck.GUARD
                else:
                    # if no peekCard info is available,
                    # link these two players logically
                    self.tied[actor.name] = target
                    self.tied[target.name] = actor
            else:
                if actor.alive:
                    winner, loser = actor, target
                else:
                    winner, loser = target, actor
                # winner must have card > loserCard (antiCards <= loserCard)
                loserCard = loser.discard[-1]
                self.antiCards[winner.name] |= set(range(Deck.GUARD,
                                                         loserCard+1))
        elif card == Deck.PRIEST:
            if actor == self.player:
                self.peekCards[target.name] = self.player.peekCard
            elif target == self.player:
                self.leakCard = actor.peekCard

        elif card == Deck.GUARD and target.alive:
            self.antiCards[target.name].add(guess)

        # final operation to ensure tied players with peekCards are unsynced
        for p in (actor, target):
            twin = self.tied[p.name]
            if twin is not None and self.peekCards[p.name]:
                self.peekCards[twin.name] = self.peekCards[p.name]
                # unsync
                self.tied[twin.name] = None
                self.tied[p.name] = None

    def deduce(self, state, unseenCards, suspectCards):
        undeducedCards = unseenCards.copy()
        equilibrium = True

        # mark peekCards as "deduced" (~seen) by decrementing undeducedCards
        # undeducedCards apply only to players whose cards haven't been peeked
        for p in state.players:
            if p != self.player and self.peekCards[p.name] is not None:
                undeducedCards[self.peekCards[p.name]] -= 1

        # synchronize deductions for "linked" players (who tied via BARON)
        self.syncLogic(state, undeducedCards)

        # create list of suspect cards for each player
        for p in state.players:
            if self.peekCards[p.name] is not None:
                suspectCards[p.name] = {self.peekCards[p.name]:1}
            elif p != self.player:
                suspectCards[p.name] = undeducedCards.copy()
                for antiCard in self.antiCards[p.name]:
                    suspectCards[p.name][antiCard] = 0

                suspectCount = 0
                for card, freq in suspectCards[p.name].items():
                    if freq > 0:
                        suspectCard = card
                        suspectCount += 1

                if suspectCount == 1:
                    # we've process of elimination-ed and now we have to
                    # start over since undeducedCards needs to be updated &
                    # dependencies on undeducedCards have to be reevaluated
                    self.peekCards[p.name] = suspectCard
                    twin = self.tied[p.name]
                    if twin is not None:
                        self.peekCards[twin.name] = suspectCard
                        # unsync players with identical hands
                        self.tied[twin.name] = None
                        self.tied[p.name] = None
                    # equilibrium = False triggers another iteration
                    equilibrium = False

        return equilibrium


    def syncLogic(self, state, unseenCards):
        # synchronize logic for players known to have same card (linked)
        for p in state.players:
            twin = self.tied[p.name]
            if twin is not None:
                if self.peekCards[p.name] is not None:
                    print "Error: trying to unsync peekCards in syncLogic"

                # only unseen duplicate cards can tie
                for card, freq in unseenCards.items():
                    if freq < 2:
                        self.antiCards[p.name].add(card)
                self.antiCards[p.name] |= self.antiCards[twin.name]

    def printSuspectCards(self, state, suspectCards):
        print "-"*16, "POTENTIAL HANDS", "-"*17
        for p in state.players:
            if p != self.player and p.alive:
                print p.name
                print [str(card)*n for card, n in suspectCards[p.name].items()]
                print

    def old_update(self, state):
        me = self.myPlayer(state)
        them = self.myOpponents(state)
        if me.alive:
            if state.currAction is None:
                # game just started
                self.dists = {}
                self.cardsLeft = Deck.cardDist[:]
                for p in them:
                    self.dists[p.name] = self.cardsLeft[:]
                for card in me.hand:
                    self.newInfo(state, card, None)
            else:
                print "before", self.dists
                card, actor, target, guess = state.currAction
                if actor is not me:
                    self.newInfo(state, card, actor)
                    if card in self.dists[actor.name]:
                        self.dists[actor.name] = self.cardsLeft[:]
                if card == Deck.COUNTESS:
                    pass
                elif card == Deck.KING:
                    if target is not None:
                        if actor is me:
                            self.dists[target.name] = [me.peekCard]
                            self.newInfo(state, me.hand[0], target)
                        elif target is me:
                            self.dists[actor.name] = [me.peekCard]
                            self.newInfo(state, me.hand[0], actor)
                        else:
                            temp = self.dists[actor.name][:]
                            self.dists[actor.name] = self.dists[target.name][:]
                            self.dists[target.name] = temp
                    if actor is not me and self.dists[actor.name].count(Deck.COUNTESS) > 0:
                        self.dists[actor.name].remove(Deck.COUNTESS)

                    pass
                elif card == Deck.PRINCE:
                    if target is me:
                        self.newInfo(state, me.hand[0], None)
                    else:
                        self.newInfo(state, target.discard[-1], target)
                    if actor is not me and self.dists[actor.name].count(Deck.COUNTESS) > 0:
                        self.dists[actor.name].remove(Deck.COUNTESS)
                elif card == Deck.HANDMAIDEN:
                    pass
                elif card == Deck.BARON:
                    if target is not None:
                        if actor is me:
                            if target.alive:
                                self.newInfo(state, me.hand[0], target)
                                self.dists[target.name] = [me.hand[0]]
                            else:
                                self.newInfo(state, target.discard[-1], target)
                        elif target is me:
                            if actor.alive:
                                self.newInfo(state, me.hand[0], actor)
                                self.dists[actor.name] = [me.hand[0]]
                            else:
                                self.newInfo(state, actor.discard[-1], actor)
                        else:
                            if actor.alive:
                                if target.alive:
                                    if len(self.dists[actor.name]) == 1:
                                        self.dists[target.name] = self.dists[actor.name][:]
                                    elif len(self.dists[target.name]) == 1:
                                        self.dists[actor.name] = self.dists[target.name][:]
                                    else:
                                        for c in Deck.cardSet:
                                            if self.dists[actor.name].count(c) == 1:
                                                self.dists[actor.name].remove(c)
                                            if self.dists[target.name].count(c) == 1:
                                                self.dists[target.name].remove(c)
                                        if len(self.dists[actor.name]) == 2:
                                            del self.dists[actor.name][1]
                                            self.dists[target.name] = self.dists[actor.name][:]
                                        elif len(self.dists[target.name]) == 2:
                                            del self.dists[target.name][1]
                                            self.dists[actor.name] = self.dists[target.name][:]
                                else:
                                    self.newInfo(state, target.discard[-1], target)
                            else:
                                    self.newInfo(state, actor.discard[-1], actor)
                elif card == Deck.PRIEST:
                    # only care about targeting others (for now)
                    if actor is me and target is not None:
                        self.newInfo(state, me.peekCard, target)
                        self.dists[target.name] = [me.peekCard]
                elif card == Deck.GUARD:
                    if target is not me and target is not None:
                        if target.alive:
                            while self.dists[target.name].count(guess) > 0:
                                self.dists[target.name].remove(guess)
                        else:
                            self.newInfo(state, target.discard[-1], target)

                if state.currPlayer is me:
                    self.newInfo(state, me.hand[1], None)

            print "after", self.dists
        return

    def newInfo(self, state, card, player):
        if player is None or self.dists[player.name] != [card]:
            self.cardsLeft.remove(card)
            for p in self.myOpponents(state):
                if len(self.dists[p.name]) > 1 and self.dists[p.name].count(card) > 0:
                    self.dists[p.name].remove(card)
        return

def main():
    bot = InfoBot()
    bot.run()

if __name__ == "__main__":
    main()
