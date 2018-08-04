from . base import BaseGame
from .. import colors


clist = [
    colors.Off,
    colors.Red,
    colors.Orange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Fuchsia
]


class GameMenu(BaseGame):
    def setup(self, count):
        self.count = count

    def reset(self):
        self.selected = None

    def frame(self):
        self.matrix.clear()
        self.selected = None
        for i in range(self.count):
            self.matrix.set(i, i, clist[i % len(clist)])
            if self.buttons.get(i, i):
                self.selected = i
