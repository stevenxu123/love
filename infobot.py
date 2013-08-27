from deck import *
from dumbbot import *

class InfoBot(DumbBot):

    def update(self, state):
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
