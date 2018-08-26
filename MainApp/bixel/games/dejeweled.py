from . base import BaseGame
from .. import colors
from .. import font
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

    def find_empty_cols(self):
        res = []
        for x in range(16):
            if sum([self.get(x, y) for y in range(16)]) == 0:
                res.append(x)

        cont = []
        for i in range(15, -1, -1):
            if i not in res:
                break
            else:
                cont.append(i)

        return list(set(res) - set(cont))

    def highlight_col(self, col):
        for y in range(16):
            self.set(col, y, HIGHLIGHT)

    def delete_col(self, col):
        for x in range(col, 15, 1):
            for y in range(16):
                self.set(x, y, self.get(x + 1, y))

        for y in range(16):
            self.set(15, y, 0)


class dejeweled(BaseGame):
    def reset(self):
        self.jewels = Jewels()
        self.deleted = False
        self.groups = []
        self.empty_cols = []
        self.clearing_groups = False
        self.highlighted = False

        self._step = 0
        self.moves = 0

    def frame(self):
        if self.jewels.check_empty():
            score = '{}'.format(self.moves)
            w, h = font.str_dim(score)
            x = (16 - w) // 2
            self.matrix.drawText(score, x=(x - 1), y=4, color=colors.Blue)

            if self.buttons.int_high():
                self.reset()
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
            elif self.empty_cols:
                if self._step % 15 == 0:
                    if not self.highlighted:
                        self.highlighted = True
                        for col in self.empty_cols:
                            self.jewels.highlight_col(col)
                    else:
                        self.highlighted = False
                        for col in reversed(self.empty_cols):
                            self.jewels.delete_col(col)
                        self.empty_cols = []
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
                    self.empty_cols = self.jewels.find_empty_cols()

            for y in range(16):
                for x in range(16):
                    self.matrix.set(x, y, clist[self.jewels.get(x, y)])

        self._step += 1
