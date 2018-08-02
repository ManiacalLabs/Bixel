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
        self.table = table

        if table:
            self.height = len(table)
            self.width = len(table[0])
        else:
            self.height = height
            self.width = width
            self.genNewTable()

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
        val_sum = 0
        count = 0

        if y > 0:
            if self.table[y - 1][x]:
                count = count + 1
                val_sum += self.table[y - 1][x]
            if x > 0:
                if self.table[y - 1][x - 1]:
                    count = count + 1
                    val_sum += self.table[y - 1][x - 1]
            if self.width > (x + 1):
                if self.table[y - 1][x + 1]:
                    count = count + 1
                    val_sum += self.table[y - 1][x + 1]

        if x > 0:
            if self.table[y][x - 1]:
                count = count + 1
                val_sum += self.table[y][x - 1]
        if self.width > (x + 1):
            if self.table[y][x + 1]:
                count = count + 1
                val_sum += self.table[y][x + 1]

        if self.height > (y + 1):
            if self.table[y + 1][x]:
                count = count + 1
                val_sum += self.table[y + 1][x]
            if x > 0:
                if self.table[y + 1][x - 1]:
                    count = count + 1
                    val_sum += self.table[y + 1][x - 1]
            if self.width > (x + 1):
                if self.table[y + 1][x + 1]:
                    count = count + 1
                    val_sum += self.table[y + 1][x + 1]

        return count, val_sum

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
        for y in range(0, self.height):
            for x in range(0, self.width):
                count, val_sum = self.liveNeighbours(y, x)

                if self.table[y][x] == 0:
                    if count == 3:
                        nt[y][x] = 2 if (val_sum / count) > 1.1 else 1
                else:
                    if (count < 2) or (count > 3):
                        nt[y][x] = 0

        self.table = nt

COLOR_TABLE = [
    colors.Off,
    colors.Red,
    colors.Blue,
    colors.Fuchsia
]

class GameOfLife(BaseGame):

    def setup(self, toroidal=False, frames_per_step=10):
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
                self.matrix.set(x, y, COLOR_TABLE[col])
                x = x + 1
            y = y + 1
            x = 0

    def frame(self):
        for x, y in self.buttons.int_high():
            if self._table.table[y][x] == 2:
                self._table.table[y][x] = 1
            elif self._table.table[y][x] == 1:
                self._table.table[y][x] = 0
            else:
                self._table.table[y][x] = 2
        if self._step % self.frames_per_step == 0:
            # start = time.time()
            self._table.turn()
            self.show_table()
            # print(time.time() - start)
        else:
            self.show_table()
        self._step += 1