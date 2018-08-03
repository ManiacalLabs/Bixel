import random
import copy
from collections import deque
import time
import threading
from . base import BaseGame
from .. import colors


class LightsOut(BaseGame):

    def setup(self):
        self.hue_map = colors.diagonal_matrix(16)[::-1]
        # self.hue_map = colors.genVector(16, 16)

    def reset(self):
        self.table = []

        random.seed(time.time())
        for y in range(0, self.matrix.height):
            self.table.append([])
            for x in range(0, self.matrix.width):
                self.table[y].append(random.randint(0, 1))

        self._step = 0

    def show_table(self):

        x = 0
        y = 0
        for row in self.table:
            for col in row:
                if col:
                    c = colors.hue2rgb((self.hue_map[y][x] + self._step) % 255)
                    # c = colors.hue_helper(self.hue_map[y][x], 16, self._step)
                    self.matrix.set(x, y, c)
                else:
                    self.matrix.set(x, y, colors.Off)
                x = x + 1
            y = y + 1
            x = 0

    def toggle(self, x, y):
        self.table[y][x] = not bool(self.table[y][x])

        if y > 0:
            self.table[y-1][x] = not bool(self.table[y-1][x])
        if y < (self.matrix.height-1):
            self.table[y+1][x] = not bool(self.table[y+1][x])
        if x > 0:
            self.table[y][x-1] = not bool(self.table[y][x-1])
        if x < (self.matrix.width-1):
            self.table[y][x+1] = not bool(self.table[y][x+1])

    def frame(self):
        for x, y in self.buttons.int_high():
            self.toggle(x, y)
        self.show_table()
        self._step += 1
        if self._step > 255:
            self._step = 0