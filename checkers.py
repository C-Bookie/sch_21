
import random
import math

import numpy as np
from gym import spaces

class Game():
    def __init__(self):
        self.size = 8
        self.printOut = False

    #todo action=X,Y,Dir    0<=X<size 0<=Y<size 0<=Dir<4
    #        self.action_space = spaces.Discrete(2)  #shall define the boolean input, True for 'hit me'
    #        self.observation_space = spaces.Discrete(52)    #an arrray representing the deck, each element is true if the bot has the card in their hand

    def reset(self):
        assert self.size != None
        self.board = [[0 for _x in range(self.size)] for _y in range(self.size)]
        for player in range(2): #1 for player 1, 2 for 2, 3 for 1 king, 4 for 2 king
            for y in range(int(self.size*(3/8))):
                for x in range(int(self.size / 2)):
                    if (self.printOut): print(str(x*2+((y+player)%2)) + ", " + str(y if player == 0 else self.size-y-1) + " = " + str(player + 1))
                    self.board[y if player == 0 else self.size-y-1][x*2+((y+player)%2)] = player + 1

    def render(self):
        def div():
            r = ""
            for i in range(self.size):
                r += "+---"
            return r + "+\n"

        r = ""
        for y in range(self.size):
            r += div()
            for x in range(self.size):
                fill = "~" if (x+y)%2 else " "
                r += "|" + fill
                cell = self.board[self.size-y-1][x]
                if cell == 0:
                    r += fill
                elif cell == 1:
                    r += "D"
                elif cell == 2:
                    r += "V"
                elif cell == 3:
                    r += "B"
                elif cell == 4:
                    r += "M"
                else :
                    r += "?"
                r += fill
            r += "|\n"
        r+=div()
        print(r)

if __name__ == '__main__':
    game = Game()
    game.reset()
    game.render()




