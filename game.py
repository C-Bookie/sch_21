
import random
import math

players = 5
deck = []
hands = []
scores = [0]*players

suites = ["clubs", "diamonds", "hearts", "spades"]
ranks = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"]

def hitMe():
    if len(deck) > 0:
        choice = random.randint(0, len(deck)-1)
        return deck.pop(choice)
    else:
        raise Exception

def hitPlayer(p):
    hands[p].append(hitMe())
    return getScore(p) > 21

def init(p):
    global deck
    deck = []
    for i in range(52):
        deck.append(i)

    global hands
    hands = []
    for i in range(p):
        hands.append([])
        for j in range(2):
            hands[i].append(hitMe())

def translator(n):
    return "the " + ranks[n%13] + " of " + suites[math.floor(n/13)]

def getScore(p):
    h = hands[p]
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

def printHands():
    for idxI, i in enumerate(hands):
        msg = "Player " + str(idxI+1) + " holds "
        for idxJ, j in enumerate(i):
            msg += translator(j)
            if idxJ == len(i)-2:
                msg += " and "
            elif idxJ < len(i)-2:
                msg += ", "
        score = getScore(idxI)
        if score > 21:
            msg += " busting with a total of "
        else:
            msg += " for a total of "
        msg += str(score)
        print(msg)

def basicBot(p):
    return getScore(p) < 15

def test1():
    init(1)
    while not hitPlayer(0):
        continue
    printHands()

def test2():
    player = 0
    games = 100
    while games > 0:
        init(players)
        for i in range(len(hands)):
            j = (i+player)%len(hands)
            while basicBot(j):
                hitPlayer(j)
        printHands()
        winners = [0]
        toBeat = getScore(0)
        i = 1
        while i < len(hands):
            s = getScore(i)
            if (s > toBeat):
                winners = [i]
                toBeat = s
            elif (s == toBeat):
                winners.append(i)
            i += 1
        if (len(winners) == 1):
            print("Player " + str(winners[0]+1) + " wins")
            global scores
            scores[winners[0]] += 1
        else:
            msg = "Players "
            for idxI, i in enumerate(winners):
                msg += str(i+1)
                if idxI== len(winners)-2:
                    msg += " and "
                elif idxI < len(winners)-2:
                    msg += ", "
            print(msg + " drew")
        print("-------------------------")

        player=(player+1)%len(hands)
        games -= 1
    print(scores)


if __name__ == '__main__':
    test2()




