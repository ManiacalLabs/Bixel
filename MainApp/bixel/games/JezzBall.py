from . base import BaseGame
from .. import colors
from random import randint, choice


class Ball():
    def __init__(self):
        self.x = randint(0, 15)
        self.y = randint(0, 15)
        self.x_dir = choice([-1, 1])
        self.y_dir = choice([-1, 1])


class JezzBall(BaseGame):
    def setup(self, frames_per_step=5):
        self.frames_per_step = frames_per_step

    def reset(self):
        self.balls = []
        self.balls.append(Ball())
        self.balls.append(Ball())
        self.balls.append(Ball())
        self._step = 0

    def frame(self):
        self.matrix.clear()
        c = colors.hue2rgb((self._step * 2) % 256)
        for b in self.balls:
            self.matrix.set(b.x, b.y, c)

        hit_paddle = False
        # for x, y in self.buttons.pressed():
        #     self.matrix.set(x, y - 1, colors.Red)
        #     self.matrix.set(x, y, colors.Red)
        #     self.matrix.set(x, y + 1, colors.Red)
        #     if self.y in [y - 1, y, y + 1]:
        #         if self.x_dir == -1 and x == (self.x - 1):
        #             self.x_dir = 1
        #             hit_paddle = True
        #         elif self.x_dir == 1 and x == (self.x + 1):
        #             self.x_dir = -1
        #             hit_paddle = True

        if self._step % self.frames_per_step == 0:
            for b in self.balls:
                if not hit_paddle:
                    if b.x == 0:
                        b.x_dir = 1
                    elif b.x == 15:
                        b.x_dir = -1

                    if b.y == 0:
                        b.y_dir = 1
                    elif b.y == 15:
                        b.y_dir = -1

                b.x += b.x_dir
                b.y += b.y_dir

        self._step += 1


