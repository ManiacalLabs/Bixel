from . base import BaseGame
from .. import colors
from .. util import srange
from random import randint, choice
from time import time
from .. import font

clist = [
    colors.Off,
    colors.Red,
    colors.Green
]

OPEN = 0
FENCE = 1
CLOSED = 2


class Ball():
    def __init__(self):
        self.x = randint(0, 15)
        self.y = randint(0, 15)
        self.x_dir = choice([-1, 1])
        self.y_dir = choice([-1, 1])


class Field:
    def __init__(self):
        self.reset()

    def reset(self):
        self.matrix = [[0 for x in range(16)] for y in range(16)]
        self._reset_visited()

    def _reset_visited(self):
        self.__visited = [[False for x in range(16)] for y in range(16)]

    def print(self):
        for row in self.matrix:
            print(row)

    def get(self, x, y):
        return self.matrix[y][x]

    def set(self, x, y, v):
        self.matrix[y][x] = v

    def add_fence(self, a, b, balls):
        xa, ya = a
        xb, yb = b
        balls = [(b.x, b.y) for b in balls]

        if xa == xb:
            for y in srange(ya, yb):
                if not (xa, y) in balls:
                    if self.get(xa, y) == OPEN:
                        self.set(xa, y, 1)
                else:
                    break
        elif ya == yb:
            for x in srange(xa, xb):
                if not (x, ya) in balls:
                    if self.get(x, ya) == OPEN:
                        self.set(x, ya, 1)
                else:
                    break
        else:
            return False
        return True

    def _find_group(self, x, y):
        if self.get(x, y) != OPEN:
            self.__visited[y][x] = True
        if self.__visited[y][x]:
            return []
        res = [(x, y)]
        self.__visited[y][x] = True
        val = self.get(x, y)

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
                if len(group) >= 1:
                    group = sorted(group, key=lambda coords: coords[1])
                    groups.append(group)
        return groups

    def percent_open(self):
        c = 0
        for x in range(16):
            for y in range(16):
                if self.get(x, y) == OPEN:
                    c += 1
        return c / 256


class JezzBall(BaseGame):
    def setup(self, frames_per_step=5):
        self.frames_per_step = frames_per_step

    def reset(self, balls=1):
        self.win = False
        self.win_step = 0

        self.field = Field()

        self.balls = []
        for _ in range(balls):
            self.balls.append(Ball())

        self._step = 0

    def frame(self):
        self.matrix.clear()

        if self.win:
            for x in range(self.win_step):
                self.matrix.drawLine(x, 0, x, 15, colors.Red)
            self.matrix.drawText('LVL', x=2, y=0, color=colors.Blue)
            lvl = '{}'.format(len(self.balls))
            w, h = font.str_dim(lvl)
            x = (16 - w) // 2
            self.matrix.drawText(lvl, x=x, y=8, color=colors.Blue)

            if self._step % 5 == 0:
                self.win_step += 1

            if self.win_step >= 18:
                self.win = False
        else:
            for y in range(16):
                for x in range(16):
                    self.matrix.set(x, y, clist[self.field.get(x, y)])

            # c = colors.hue2rgb((self._step * 2) % 256)
            c = colors.Blue
            for b in self.balls:
                self.matrix.set(b.x, b.y, c)

            pressed = self.buttons.pressed()
            if len(pressed) >= 2:
                if self.field.add_fence(pressed[0], pressed[1], self.balls):
                    groups = self.field.find_groups()
                    for g in groups:
                        close = True
                        for b in self.balls:
                            if (b.x, b.y) in g:
                                close = False
                                break
                        if close:
                            for x, y in g:
                                self.field.set(x, y, CLOSED)

            if self._step % self.frames_per_step == 0:
                for b in self.balls:
                    x_dir = b.x_dir
                    y_dir = b.y_dir

                    if b.x == 0:
                        b.x_dir = 1
                    elif b.x == 15:
                        b.x_dir = -1
                    elif b.x_dir == 1 and self.field.get(b.x + 1, b.y) != OPEN:
                        b.x_dir = -1
                    elif b.x_dir == -1 and self.field.get(b.x - 1, b.y) != OPEN:
                        b.x_dir = 1

                    if b.y == 0:
                        b.y_dir = 1
                    elif b.y == 15:
                        b.y_dir = -1
                    elif b.y_dir == 1 and self.field.get(b.x, b.y + 1) != OPEN:
                        b.y_dir = -1
                    elif b.y_dir == -1 and self.field.get(b.x, b.y - 1) != OPEN:
                        b.y_dir = 1

                    if (b.x_dir == x_dir and b.y_dir == y_dir) and (b.x != 0 and b.x != 15 and b.y != 0 and b.y != 15):
                        if self.field.get(b.x + b.x_dir, b.y + b.y_dir) != OPEN:
                            b.x_dir *= -1
                            b.y_dir *= -1

                    b.x += b.x_dir
                    b.y += b.y_dir

            if self.field.percent_open() <= 0.10:
                self.reset(balls=len(self.balls) + 1)
                self.win = True

        self._step += 1


