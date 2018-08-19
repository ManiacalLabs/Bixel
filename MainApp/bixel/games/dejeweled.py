from . base import BaseGame
from .. import colors
from random import randint


clist = [
    colors.Off,  # no jewel
    colors.Red,
    colors.DarkOrange,
    colors.Green,
    colors.Blue,
    colors.Fuchsia,
    colors.White  # highlight
]

HIGHLIGHT = len(clist) - 1


class Jewels:
    def __init__(self):
        self.reset()

    def reset(self):
        self.matrix = [[self._new_jewel() for x in range(16)] for y in range(16)]
        self._reset_visited()

    def _new_jewel(self):
        return randint(1, len(clist) - 2)

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
        if self.get(x, y) == 0:
            return False
        for i in range(y, 0, -1):
            self.set(x, i, self.get(x, i - 1))
        self.set(x, 0, 0)
        return True

    def highlight(self, x, y):
        if self.get(x, y) == 0:
            return False
        self.set(x, y, HIGHLIGHT)
        return True

    def delete_group(self, group):
        for x, y in group:
            # self.delete(x, y)
            self.set(x, y, HIGHLIGHT)

    def drop_highlighted(self):
        for y in range(1, 16, 1):
            for x in range(16):
                if self.get(x, y) == HIGHLIGHT:
                    self.delete(x, y)

    def highlight_group(self, group):
        for x, y in group:
            self.set(x, y, HIGHLIGHT)

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
                    # ensure ordered by y asc so they are deleted correctly
                    group = sorted(group, key=lambda coords: coords[1])
                    groups.append(group)
        return groups

    def check_empty(self):
        return sum([sum(row) for row in self.matrix]) == 0


class dejeweled(BaseGame):
    def reset(self):
        self.jewels = Jewels()
        self.deleted = False
        self.groups = []
        self.clearing_groups = False
        self.highlighted = False

        self._step = 0
        self.moves = 0

    def frame(self):
        if self.jewels.check_empty():
            for i in range(self.moves):
                if i < 256:
                    self.matrix.pixels.set(i, colors.Red)
        else:
            if self.groups:
                if self._step % 15 == 0:
                    if not self.highlighted:
                        self.highlighted = True
                        for group in self.groups:
                            self.jewels.highlight_group(group)
                    else:
                        self.highlighted = False
                        self.jewels.drop_highlighted()
                        self.groups = []
            else:
                pressed = False
                for x, y in self.buttons.int_high():
                    if self.jewels.highlight(x, y):
                        pressed = True
                if pressed:
                    self.moves += 1
                    self.jewels.drop_highlighted()
                    # print(self.moves)

                if self._step % 15 == 0:
                    self.groups = self.jewels.find_groups()

            for y in range(16):
                for x in range(16):
                    self.matrix.set(x, y, clist[self.jewels.get(x, y)])

        self._step += 1
