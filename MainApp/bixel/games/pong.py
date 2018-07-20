from . base import BaseGame
from .. import colors
from random import randint, choice


class pong(BaseGame):
    def setup(self, frames_per_step=4):
        self.circles = []
        self.frames_per_step = frames_per_step

    def reset(self):
        self.x = randint(0, 15)
        self.y = randint(0, 15)
        self.x_dir = choice([-1,1])
        self.y_dir = choice([-1,1])
        self._step = 0

    def frame(self):
        self.matrix.clear()
        self.matrix.set(self.x, self.y, colors.Green)

        if self._step % self.frames_per_step == 0:
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

        self._step += 1


