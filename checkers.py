
from gym import spaces
import numpy as np

class Game():
    def __init__(s):
        s.sizeX = 8
        s.sizeY = 8
        s.board = [[0 for _x in range(s.sizeX)] for _y in range(s.sizeY)]

        s.counter = 0

        s.printOut = False
        s.done = False
        s.rewardBuffer = 0
        s.defaultReward = 50

        s.actSpace = spaces.Box([0,0,0,0], [s.sizeY, s.sizeX, 2, 2]) #2 axis of movment, Y & X (Y should proberbly be flipped for easeyer traning)
        s.obsSpace = spaces.Box(0, 2**3, (s.sizeY, s.sizeX), np.byte) #states: notEmpty, player, king

    def reset(s):
        s.board = [[0 for _x in range(s.sizeX)] for _y in range(s.sizeY)]
        for player in range(2):
            for y in range(int(s.sizeY*(3/8))):
                for x in range(int(s.sizeX / 2)):
                    #print(str(x*2+((y+player)%2)) + ", " + str(y if player == 0 else s.sizeY-y-1) + " = " + str(player + 1))
                    s.board[y if player == 0 else s.sizeY-y-1][x*2+((y+player)%2)] = (player*2**1) + 1
        s.counter = 0
        return s.observation()

    def reward(s):
        r=s.rewardBuffer
        s.rewardBuffer=0
        return r

    def observation(s):
        return np.ndarray(s.board)

    #currently only functionality to make one move per turn, no jumping chains
    def step(s, action):    #action=[Yposition, Xposition, Ydirection, Xdirection]
        #validators
        if not (s.board[action[0]][action[1]] & 0b001):
            s.rewardBuffer -= s.defaultReward/10    #cell empty

        if s.board[action[0]][action[1]] & 0b010:
            s.rewardBuffer -= s.defaultReward/10    #piece not yours

        if (not s.board[action[0]][action[1]] & 0b100) and action[2] == 0:
            s.rewardBuffer -= s.defaultReward/10    #invalid direction, not king

        if not ((action[0] + (action[2] * 2 - 1) in range(s.sizeY) and action[1] + (action[3] * 2 - 1) in range(s.sizeX))):
            s.rewardBuffer -= s.defaultReward / 10  #move falls off board

        if s.rewardBuffer >= 0: #if the move is valid so far
            if s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] & 0b001:   #if space is free
                s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = s.board[action[0]][action[1]]   #copy
                s.board[action[0]][action[1]] = 1   #remove
                if action[0] + (action[2] * 2 - 1) == s.sizeY-1:    #if upgrade to king
                    s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = s.board[action[0]][action[1]] = s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = s.board[action[0]][action[1]] | 0b100
            else:
                if (action[0] + (action[2] * 4 - 2) in range(s.sizeY) and action[1] + (action[3] * 4 - 2) in range(s.sizeX)):   #if you don't jump off the board
                    if s.board[action[0] + (action[2] * 4 - 2)][action[1] + (action[3] * 4 - 2)] & 0b001:   #and the space to jump to is free
                        if s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] & 0b010:   #and your acctually attacking an enimy
                            s.board[action[0] + (action[2] * 4 - 2)][action[1] + (action[3] * 4 - 2)] = s.board[action[0]][action[1]]  # copy
                            s.board[action[0]][action[1]] = 1  # remove
                            s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = 1   #take piece
                            s.rewardBuffer += s.defaultReward / 10  #reward
                            if action[0] + (action[2] * 2 - 1) == s.sizeY - 1:  #if upgrade to king
                                s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = s.board[action[0]][action[1]] = s.board[action[0] + (action[2] * 2 - 1)][action[1] + (action[3] * 2 - 1)] = s.board[action[0]][action[1]] | 0b100
                        else:
                            s.rewardBuffer -= s.defaultReward / 10  # jumping falls off board
                    else:
                        s.rewardBuffer -= s.defaultReward / 10  #jumping falls off board
                else:
                    s.rewardBuffer -= s.defaultReward / 10  #jumping falls off board

        if s.rewardBuffer >= 0: #if the move was valid
            s.counter+=1

        return s.observation(), s.reward(), s.done, {s.counter}

    def render(s):
        def div():
            r = ""
            for i in range(s.sizeX):
                r += "+---"
            return r + "+\n"

        r = ""
        for y in range(s.sizeY):
            r += div()
            for x in range(s.sizeX):
                fill = "~" if (x+y)%2 else " "
                r += "|" + fill
                cell = s.board[s.sizeY-y-1][x]
                if not cell & 0b001:
                    r += fill
                elif cell & 0b010 > 0:
                    if cell & 0b100 > 0:
                        r += "B"
                    else:
                        r += "D"
                else :
                    if cell & 0b100 > 0:
                        r += "M"
                    else:
                        r += "V"
                r += fill
            r += "|\n"
        r+=div()
        print(r)

if __name__ == '__main__':
    game = Game()
    game.reset()
    game.render()




