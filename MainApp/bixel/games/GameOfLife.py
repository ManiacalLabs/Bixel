import random
import copy
from collections import deque
import time
import threading
from . base import BaseGame
from .. import colors

class Table:

    def __init__(self, height, width, rand_max, table=None):
        self.toroidal = True
        self._rand_max = rand_max
        if table:
            self.table = table
            self.height = len(table)
            self.width = len(table[0])
        else:
            self.height = height
            self.width = width
            self.genNewTable()

        self._oldStates = deque()
        for i in range(3):
            self._oldStates.append([])

    def genNewTable(self):
        self.table = []

        random.seed(time.time())
        for y in range(0, self.height):
            self.table.append([])
            for x in range(0, self.width):
                rand = random.randint(0, self._rand_max)
                if rand == 0:
                    self.table[y].append(1)
                else:
                    self.table[y].append(0)

    def liveNeighbours(self, y, x):
        """Returns the number of live neighbours."""
        count = 0
        if y > 0:
            if self.table[y - 1][x]:
                count = count + 1
            if x > 0:
                if self.table[y - 1][x - 1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y - 1][x + 1]:
                    count = count + 1

        if x > 0:
            if self.table[y][x - 1]:
                count = count + 1
        if self.width > (x + 1):
            if self.table[y][x + 1]:
                count = count + 1

        if self.height > (y + 1):
            if self.table[y + 1][x]:
                count = count + 1
            if x > 0:
                if self.table[y + 1][x - 1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y + 1][x + 1]:
                    count = count + 1

        if self.toroidal:
            if y == 0:
                if self.table[self.height - 1][x]:
                    count = count + 1
            if y == self.height - 1:
                if self.table[0][x]:
                    count = count + 1
            if x == 0:
                if self.table[y][self.width - 1]:
                    count = count + 1
            if x == self.width - 1:
                if self.table[y][0]:
                    count = count + 1

        return count

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbours = self.liveNeighbours(y, x)
                if self.table[y][x] == 0:
                    if neighbours == 3:
                        nt[y][x] = 1
                else:
                    if (neighbours < 2) or (neighbours > 3):
                        nt[y][x] = 0

        self._oldStates.append(self.table)
        if len(self._oldStates) > 3:
            self._oldStates.popleft()

        self.table = nt

    def checkStable(self):
        for t in self._oldStates:
            if self.table == t:
                return True
        return False


class GameOfLife(BaseGame):

    def setup(self, color=colors.Red, bg=colors.Off, toroidal=False, frames_per_step=10):
        self._color = color
        self._bg = bg
        self.toroidal = toroidal
        self._finishCount = 0
        self.frames_per_step = frames_per_step

    def reset(self):
        self._table = Table(self.matrix.height, self.matrix.width, 1, None)
        self._table.toroidal = self.toroidal
        self._step = 0

    def show_table(self):
        x = 0
        y = 0
        for row in self._table.table:
            for col in row:
                if col == 0:
                    self.matrix.set(x, y, self._bg)
                else:
                    self.matrix.set(x, y, self._color)
                x = x + 1
            y = y + 1
            x = 0

    def frame(self):
        for x, y in self.buttons.int_high():
            if self._table.table[y][x]:
                self._table.table[y][x] = 0
            else:
                self._table.table[y][x] = 1
        if self._step % self.frames_per_step == 0:
            self._table.turn()
            self.show_table()
            if self._table.checkStable():
                self._finishCount += 1
                if self._finishCount > 10:
                    self._table.genNewTable()
                    self._finishCount = 0
                    self.animComplete = True
        else:
            self.show_table()
        self._step += 1