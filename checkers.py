
from gym import spaces

class Game():
    def __init__(self):
        size = 8
        self.sizeX = size
        self.sizeY = size

        self.printOut = False

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(0, (self.sizeY, self.sizeX, 3)) #states: empty, player, king

    def reset(self):
        assert self.sizeX != None
        assert self.sizeY != None
        self.board = [[0 for _x in range(self.sizeX)] for _y in range(self.sizeY)]
        for player in range(2):
            for y in range(int(self.sizeY*(3/8))):
                for x in range(int(self.sizeX / 2)):
                    if (self.printOut):print(str(x*2+((y+player)%2)) + ", " + str(y if player == 0 else self.sizeY-y-1) + " = " + str(player + 1))
                    self.board[y if player == 0 else self.sizeY-y-1][x*2+((y+player)%2)] = player + 1

    def reward(self):
        if (self.prize):
            self.prize = False
            return 50
        return 0

    def observation(self):
        r = []
        for i in range(52):
            r.append(i in self.hands[0])
        return np.array(r)

    def step(self):

        return self.observation(), self.reward(), self.done, {}

    def render(self):
        def div():
            r = ""
            for i in range(self.sizeX):
                r += "+---"
            return r + "+\n"

        r = ""
        for y in range(self.sizeY):
            r += div()
            for x in range(self.sizeX):
                fill = "~" if (x+y)%2 else " "
                r += "|" + fill
                cell = self.board[self.sizeY-y-1][x]
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




