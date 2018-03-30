
import random
import math

class Game():
    players = 5
    deck = []
    hands = []
    scores = [0]*players

    suites = ["clubs", "diamonds", "hearts", "spades"]
    ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"]

    printOut = False
    prize = False

    def debug(self, msg):
        if (self.printOut):
            print(msg)

    def hitMe(self):
        if len(self.deck) > 0:
            choice = random.randint(0, len(self.deck)-1)
            return self.deck.pop(choice)
        else:
            raise Exception

    def hitPlayer(self, p):
        self.hands[p].append(self.hitMe())
        bust = self.getScore(p) > 21
        if bust:
            self.debug("Player " + str(p) + " busted")
        return bust

    def translator(self, n):
        return "the " + self.ranks[n%13] + " of " + self.suites[math.floor(n/13)]

    def getScore(self, p):
        h = self.hands[p]
        aces = 0
        r = 0
        for c in h:
            rank = (c%13)+1
            if rank == 1:
                aces += 1
                r += 11
            elif rank > 10:
                r += 10
            else:
                r += rank
            if r > 21 and aces > 0:
                aces -= 1
                r -= 10
        return r

    def render(self):
        self.printHand(0)

    def printHand(self, p):
        hand = self.hands[p]
        msg = "Player " + str(p + 1) + " holds "
        for idxJ, j in enumerate(hand):
            msg += self.translator(j)
            if idxJ == len(hand) - 2:
                msg += " and "
            elif idxJ < len(hand) - 2:
                msg += ", "
        score = self.getScore(p)
        if score > 21:
            msg += " busting with a total of "
        else:
            msg += " for a total of "
        msg += str(score)
        self.debug(msg)

    def printHands(self):
        for p in range(len(self.hands)):
            self.printHand(p)

    def basicPlay(self, p):
        while self.getScore(p) < 15 and not self.hitPlayer(p):  # true while returning "hit me"
            continue

    def reset(self):
        self.done = False
        self.dealer = random.randint(0, self.players-1)
        self.game()

    def reward(self):
        if (self.prize):
            self.prize = False
        return 50 if self.prize else 0

    class action_space():
        def sample(self):
            return bool(random.randint(0, 1))

    def step(self, hit): #ANN contorl
        if (hit):
            if self.hitPlayer(0):
                self.done = True
        else:
            self.currentPlayer += 1
            self.play()
        return {}, self.reward(), self.done, {}

    def game(self):
        self.deck = []
        for i in range(52):
            self.deck.append(i)

        self.hands = []
        for i in range(self.players):
            self.hands.append([])
            for j in range(2):
                self.hands[i].append(self.hitMe())

        self.currentPlayer = 0
        self.play()

    def play(self):
        while True:
            if (self.currentPlayer >= self.players):
                self.done = True
                self.printHands()

                winners = []
                toBeat = 0
                for i in range(self.players):
                    s = self.getScore(i)
                    if (s < 21):
                        if (s > toBeat):
                            winners = [i]
                            toBeat = s
                        elif (s == toBeat):
                            winners.append(i)
                    i += 1

                if (0 in winners):
                    self.prize = True

                if (len(winners) == 0):
                    self.debug("No one wins")
                elif (len(winners) == 1):
                    self.debug("Player " + str(winners[0] + 1) + " wins")
                    self.scores[winners[0]] += 1
                else:
                    msg = "Players "
                    for idxI, i in enumerate(winners):
                        msg += str(i + 1)
                        if idxI == len(winners) - 2:
                            msg += " and "
                        elif idxI < len(winners) - 2:
                            msg += ", "
                    self.debug(msg + " drew")
                self.debug("-------------------------")
                break
            j = (self.currentPlayer + self.dealer + 1) % self.players
            if (j == 0):
                break
            else:
                self.basicPlay(j)
                self.currentPlayer += 1

    def test(self):
        games = 1000
        while games > 0:
            self.debug(str(1000-games))
            self.reset()
            don = False
            i = 1
#            while self.basicPlay(0) and not don:
            while i > 0 and not don:
                obs, rew, don, inf = self.step(True)
                i -= 1
            self.step(False)
            games -= 1
        print(self.scores)


if __name__ == '__main__':
    game = Game()
    game.test()




