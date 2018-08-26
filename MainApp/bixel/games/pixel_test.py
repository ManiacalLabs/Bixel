from . base import BaseGame
from .. import colors


class pixel_test(BaseGame):
    def setup(self):
        self.circles = []

    def frame(self):
        self.matrix.clear()
        for x, y in self.buttons.pressed():
            self.matrix.set(x, y, colors.Red)
