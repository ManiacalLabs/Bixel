from . base import BaseGame
from .. import colors
from random import randint, choice


class pong(BaseGame):
    def setup(self):
        self.circles = []

    def reset(self):
        self.x = randint(0, 15)
        self.y = randint(0, 15)
        self.x_dir = choice([-1,1])
        self.y_dir = choice([-1,1])

    def frame(self):
        self.matrix.clear()
        self.matrix.set(self.x, self.y, colors.Green)

        print(self.x, self.y)

        if self.x == 0:
            self.x_dir = 1
        elif self.x == 15:
            self.x_dir = -1

        if self.y == 0:
            self.y_dir = 1
        elif self.y == 15:
            self.y_dir = -1

        self.x += self.x_dir
        self.y += self.y_dir


