from . base import BaseGame
from .. import colors
from random import randint, choice


class MatrixRainBow(BaseGame):
    def setup(self, tail=4, growthRate=4, frames_per_step=3):
        self._tail = tail
        self._growthRate = growthRate
        self.frames_per_step = frames_per_step

    def reset(self):
        self._drops = [[] for x in range(self.matrix.width)]
        self.drops = []
        self._step = 0

    def _drawDrop(self, x, y):
        color = colors.hue2rgb((y if y < self.matrix.height else (
            self.matrix.height - 1)) * (255 // self.matrix.height))
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.matrix.height:
                level = 255 - ((255 // self._tail) * i)
                self.matrix.set(x, y - i, colors.color_scale(color, level))

    def frame(self):
        if self._step % self.frames_per_step == 0:
            for _ in range(self._growthRate):
                newDrop = randint(0, self.matrix.width - 1)
                self.drops.append((newDrop, 0))

            self.matrix.clear()

            new_drops = []
            for x, y in self.drops:
                if y < (self.matrix.height + self._tail - 1):
                    self._drawDrop(x, y)
                    if y < (self.matrix.height - 1):
                        while True:
                            if self.buttons.get(x, y+1):
                                x = x + choice([1,-1])
                            else:
                                break
                        new_drops.append((x, y+1))
                    else:
                        new_drops.append((x, y+1))

            self.drops = new_drops

        self._step += 1
