from . base import BaseGame
from .. import colors


clist = [
    colors.Red,
    colors.Orange,
    colors.Yellow,
    colors.Green,
    colors.Blue,
    colors.Fuchsia
]


class GameMenu(BaseGame):
    def setup(self, runner):
        self.runner = runner

    @property
    def count(self):
        return len(self.runner.games)

    def reset(self):
        self.selected = None

    def frame(self):
        self.matrix.clear()
        self.selected = None
        for i in range(self.count):
            self.matrix.set(i, i, clist[i % len(clist)])
            if self.buttons.get(i, i):
                self.selected = i
