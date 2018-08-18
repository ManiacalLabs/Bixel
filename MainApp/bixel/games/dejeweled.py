from . base import BaseGame
from .. import colors
from random import randint


clist = [
    colors.Red,
    colors.DarkOrange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Fuchsia
]


class dejeweled(BaseGame):
    def reset(self):
        self.jewels = [[self._new_jewel() for x in range(16)] for y in range(16)]
        self.deleted = False

    def _new_jewel(self):
        return randint(0, len(clist) - 1)

    def delete_jewel(self, x, y):
        for i in range(y, 0, -1):
            self.jewels[i][x] = self.jewels[i - 1][x]
        self.jewels[0][x] = self._new_jewel()

    def find_groups(self):
        visited = [[False for x in range(16)] for y in range(16)]
        j = self.jewels
        for x in range(16):
            for y in range(16):
                if x > 0 and j[y][x - 1] == j[y][x]:
                    pass

    def frame(self):
        if self.deleted:
            pass
        else:
            self.deleted = False
            for x, y in self.buttons.int_high():
                self.delete_jewel(x, y)
                self.deleted = True

            for y in range(16):
                for x in range(16):
                    self.matrix.set(x, y, clist[self.jewels[y][x]])
