import random
import copy
from collections import deque
import time
import threading
import numpy as np
from . base import BaseGame
from .. import colors


# https://www.labri.fr/perso/nrougier/teaching/numpy/numpy.html

# Z = [[0,0,0,0,0,0],
#      [0,0,0,1,0,0],
#      [0,1,0,1,0,0],
#      [0,0,1,1,0,0],
#      [0,0,0,0,0,0],
#      [0,0,0,0,0,0]]

# def compute_neighbours(Z):
#     rows,cols = len(Z), len(Z[0])
#     N  = [[0,]*(cols)  for i in range(rows)]
#     for x in range(1,cols-1):
#         for y in range(1,rows-1):
#             N[y][x] = Z[y-1][x-1]+Z[y][x-1]+Z[y+1][x-1] \
#                     + Z[y-1][x]            +Z[y+1][x]   \
#                     + Z[y-1][x+1]+Z[y][x+1]+Z[y+1][x+1]
#     return N

# def show(Z):
#     for l in Z[1:-1]: print l[1:-1]
#     print

# def iterate(Z):
#     rows,cols = len(Z), len(Z[0])
#     N = compute_neighbours(Z)
#     for x in range(1,cols-1):
#         for y in range(1,rows-1):
#             if Z[y][x] == 1 and (N[y][x] < 2 or N[y][x] > 3):
#                 Z[y][x] = 0
#             elif Z[y][x] == 0 and N[y][x] == 3:
#                 Z[y][x] = 1
#     return Z

# show(Z)
# for i in range(4):
#     iterate(Z)
# show(Z)

class NPTable:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.genNewTable()

    def genNewTable(self):
        # rand 2d array with values between 0 and 1
        self.table = np.random.randint(0, 2, (self.height, self.width))

    def compute_neighbors(self):
        Z = self.table
        shape = len(Z), len(Z[0])
        N  = [[0,]*(shape[0])  for i in range(shape[1])]
        for x in range(1,shape[0]-1):
            for y in range(1,shape[1]-1):
                N[x][y] = Z[x-1][y-1]+Z[x][y-1]+Z[x+1][y-1] \
                        + Z[x-1][y]            +Z[x+1][y]   \
                        + Z[x-1][y+1]+Z[x][y+1]+Z[x+1][y+1]
        return N

    def turn(self):
        Z = self.table
        rows,cols = len(Z), len(Z[0])
        N = self.compute_neighbors()
        for x in range(1,cols-1):
            for y in range(1,rows-1):
                if Z[y][x] == 1 and (N[y][x] < 2 or N[y][x] > 3):
                    Z[y][x] = 0
                elif Z[y][x] == 0 and N[y][x] == 3:
                    Z[y][x] = 1
        self.table = Z





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

    def setup(self, color=colors.Red, bg=colors.Off, frames_per_step=10):
        self._color = color
        self._bg = bg
        self._finishCount = 0
        self.frames_per_step = frames_per_step

    def reset(self):
        # self._table = Table(self.matrix.height, self.matrix.width, 1, None)
        self._table = NPTable(self.matrix.height, self.matrix.width)
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
        # for x, y in self.buttons.int_high():
        #     if self._table.table[y][x]:
        #         self._table.table[y][x] = 0
        #     else:
        #         self._table.table[y][x] = 1
        if self._step % self.frames_per_step == 0:
            start = time.time()
            self._table.turn()
            print(time.time() - start)

        self.show_table()
        self._step += 1