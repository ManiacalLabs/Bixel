from . base import BaseGame
from .. import colors


clist = [
    colors.Off,
    colors.Red,
    colors.DarkOrange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Fuchsia
]


class lightbright(BaseGame):
    def reset(self):
        self.pegs = [[0 for y in range(16)] for x in range(16)]

    def frame(self):
        for x, y in self.buttons.int_high():
            self.pegs[x][y] += 1
            if self.pegs[x][y] >= len(clist):
                self.pegs[x][y] = 0
            self.matrix.set(x, y, clist[self.pegs[x][y]])