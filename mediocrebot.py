from deck import *
from infobot import *

class MediocreBot(InfoBot):

    def move(self, state):
        if not state.legalActions:
            raise Exception("The only winning move is not to play.")

        hand = self.player.hand

        maxRating = -1
        optimalMoves = []
        for legalAction in state.legalActions:
            rating = self.rate(legalAction, hand)
            if rating > maxRating:
                maxRating = rating
                optimalMoves[:] = []
                optimalMoves.append(legalAction)
            elif rating == maxRating:
                optimalMoves.append(legalAction)

        # select one of the optimal moves TODO: randomly
        return optimalMoves[0]

    def rate(self, action, hand):
        (card, actor, target, guess) = action
        suspectCards = self.suspectCards[target.name] if target else None
        if card == Deck.COUNTESS:
            return 0.4
        elif card == Deck.HANDMAIDEN:
            return 0.6
        elif target is None:
            return 0.5
        elif card == Deck.KING:
            if Deck.GUARD in hand:
                return 0
            else:
                return 0.6
        elif card == Deck.PRINCE:
            if target == self.player and Deck.PRINCESS in hand:
                return 0
            else:
                return 0.6
        elif card == Deck.BARON:
            myCard = hand[0] if hand[1] == Deck.BARON else hand[1]
            wins = sum(f for c,f in suspectCards.items() if myCard > c)
            trials = sum(f for c,f in suspectCards.items() if myCard != c)
            if trials == 0:
                return 0
            else:
                return float(wins) / trials
        elif card == Deck.PRIEST:
            if len(suspectCards) == 1:
                return 0.01
            else:
                return 0.6
        elif card == Deck.GUARD:
            if guess in suspectCards:
                return float(suspectCards[guess]) / len(suspectCards)
            else:
                return 0.01
        return 0

def main():
    bot = MediocreBot(trackCards=True)
    bot.run()

if __name__ == "__main__":
    main()
