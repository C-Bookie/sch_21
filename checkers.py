
from gym import spaces
import numpy as np

ACTIVE = 0b001
PLAYER = 0b010  #as in not you, the code is written from the perspective of the bot
KING = 0b100

class Game():
    
    def __init__(s):
        s.sizeX = 8
        s.sizeY = 8
        s.board = [[0 for _x in range(s.sizeX)] for _y in range(s.sizeY)]

        s.counter = 0

        s.printOut = False
        s.done = False
        s.rewBuf = 0    #reward buffer
        s.defRew = 50   #default reward

        s.actSpace = spaces.Box([0,0,0,0], [s.sizeY, s.sizeX, 2, 2]) #2 axis of movment, Y & X (Y should proberbly be flipped for easeyer traning)
        s.obsSpace = spaces.Box(0, 2**3, (s.sizeY, s.sizeX), np.byte) #states: notEmpty, player, king

    def reset(s):
        s.board = [[0 for _x in range(s.sizeX)] for _y in range(s.sizeY)]
        for player in range(2):
            for y in range(int(s.sizeY*(3/8))):
                for x in range(int(s.sizeX / 2)):
                    #print(str(x*2+((y+player)%2)) + ", " + str(y if player == 0 else s.sizeY-y-1) + " = " + str(player + 1))
                    s.board[y if player == 0 else s.sizeY-y-1][x*2+((y+player)%2)] = (player*PLAYER) | ACTIVE
        s.counter = 0
        return s.observation()

    def reward(s):
        r=s.rewBuf
        s.rewBuf=0
        return r

    def observation(s):
        return np.ndarray(s.board)

    #currently only functionality to make one move per turn, no jumping chains
    def step(s, act):    #action=[Yposition, Xposition, Ydirection, Xdirection]
        #validators
        sel = s.board[act[0]][act[1]]    #selected

        # if the selected cell is active and the piece is yours and your not moving a non-king backwards and the space to move to is on the board
        if sel & ACTIVE and not (sel & PLAYER) and not ((not sel & KING) and act[2] == 0) and act[0] +(act[2]*2 -1) in range(s.sizeY) and act[1] +(act[3]*2 -1) in range(s.sizeX):
            tar = s.board[act[0] +(act[2]*2 -1)][act[1] +(act[3]*2 -1)] #selected target
            if not tar & ACTIVE:   #if space is free
                if act[0] +(act[2]*2 -1) == s.sizeY-1:    #if upgrade to king
                        s.board[act[0] +(act[2]*2 -1)][act[1] +(act[3]*2 -1)] = sel | KING
                else:
                    s.board[act[0] +(act[2]*2 -1)][act[1] +(act[3] *2 -1)] = sel   #copy
                s.board[act[0]][act[1]] = 1   #remove
            else:
                if (act[0] + (act[2] * 4 - 2) in range(s.sizeY) and act[1] + (act[3] * 4 - 2) in range(s.sizeX)):   #if you don't jump off the board
                    if s.board[act[0] + (act[2] * 4 - 2)][act[1] + (act[3] * 4 - 2)] & 0b001:   #and the space to jump to is free
                        if s.board[act[0] + (act[2] * 2 - 1)][act[1] + (act[3] * 2 - 1)] & 0b010:   #and your acctually attacking an enimy
                            s.board[act[0] + (act[2] * 4 - 2)][act[1] + (act[3] * 4 - 2)] = s.board[act[0]][act[1]]  # copy
                            s.board[act[0]][act[1]] = 1  # remove
                            s.board[act[0] + (act[2] * 2 - 1)][act[1] + (act[3] * 2 - 1)] = 1   #take piece
                            s.rewBuf += s.defRew / 10  #reward
                            if act[0] + (act[2] * 2 - 1) == s.sizeY - 1:  #if upgrade to king
                                s.board[act[0] + (act[2] * 2 - 1)][act[1] + (act[3] * 2 - 1)] = s.board[act[0]][act[1]] = s.board[act[0] + (act[2] * 2 - 1)][act[1] + (act[3] * 2 - 1)] = s.board[act[0]][act[1]] | 0b100
                        else:
                            s.rewBuf -= s.defRew / 10  # jumping falls off board
                    else:
                        s.rewBuf -= s.defRew / 10  #jumping falls off board
                else:
                    s.rewBuf -= s.defRew / 10  #jumping falls off board
        else: #if the move was invalid
            s.rewBuf -= s.defRew/10    #cell empty

        if s.rewBuf >= 0: #if the move was valid
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




