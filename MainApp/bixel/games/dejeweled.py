from . base import BaseGame
from .. import colors
from random import randint


clist = [
    colors.Off,
    colors.Red,
    colors.DarkOrange,
    colors.Green,
    colors.Blue,
    colors.Fuchsia
]


class Jewels:
    def __init__(self):
        self.reset()

    def reset(self):
        self.matrix = [[self._new_jewel() for x in range(16)] for y in range(16)]
        self._reset_visited()

    def _new_jewel(self):
        return randint(1, len(clist) - 1)

    def _reset_visited(self):
        self.__visited = [[False for x in range(16)] for y in range(16)]

    def print(self):
        for row in self.matrix:
            print(row)

    def get(self, x, y):
        return self.matrix[y][x]

    def set(self, x, y, v):
        self.matrix[y][x] = v

    def delete(self, x, y):
        for i in range(y, 0, -1):
            self.set(x, i, self.get(x, i - 1))
        self.set(x, 0, 0)

    def delete_group(self, group):
        for x, y in group:
            self.delete(x, y)

    def _find_group(self, x, y):
        if self.__visited[y][x]:
            return []
        res = [(x, y)]
        self.__visited[y][x] = True
        val = self.get(x, y)
        if val == 0:
            return []
        if x < 15 and self.get(x + 1, y) == val:
            res.extend(self._find_group(x + 1, y))
        if x > 0 and self.get(x - 1, y) == val:
            res.extend(self._find_group(x - 1, y))
        if y < 15 and self.get(x, y + 1) == val:
            res.extend(self._find_group(x, y + 1))
        if y > 0 and self.get(x, y - 1) == val:
            res.extend(self._find_group(x, y - 1))

        return res

    def find_groups(self):
        self._reset_visited()
        groups = []
        for x in range(16):
            for y in range(16):
                group = self._find_group(x, y)
                if len(group) >= 4:
                    groups.append(group)
        return groups


class dejeweled(BaseGame):
    def reset(self):
        self.jewels = Jewels()
        self.deleted = False
        self.groups = []
        self.clearing_groups = False

        self._step = 0

    def frame(self):
        if self.clearing_groups:
            if self._step % 15 == 0:
                group = self.groups[0]
                self.groups = self.groups[1:]
                if not self.groups:
                    self.clearing_groups = False
                self.jewels.delete_group(group)
        else:
            self.groups = self.jewels.find_groups()
            if self.groups:
                self.clearing_groups = True
            else:
                for x, y in self.buttons.int_high():
                    self.jewels.delete(x, y)

        for y in range(16):
            for x in range(16):
                self.matrix.set(x, y, clist[self.jewels.get(x, y)])

        self._step += 1
