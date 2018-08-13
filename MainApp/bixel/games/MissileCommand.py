from . base import BaseGame
from .. import colors
from random import randint



class MissileCommand(BaseGame):
    def setup(self):
        self._tail = 4
        self._frames_per_missle_move = 10

    def reset(self):
        self.buildings = [randint(0, 3) for _ in range(16)]
        self.missiles = []
        self.explosions = []
        self._step = 0

    def _draw_missile(self, x, y, color):
        for i in range(self._tail):
            if y - i >= 0 and y - i < 16:
                level = 255 - ((255 // self._tail) * i)
                self.matrix.set(x, y - i, colors.color_scale(color, level))

    def _draw_missiles(self):
        for m in self.missiles:
            self._draw_missile(m[0], m[1], colors.Red)

    def _draw_explosions(self, update):
        exp = []
        for e in self.explosions:
            self.matrix.drawCircle(e[0], e[1], e[2], colors.Green)
            if update:
                if e[2] <= 5:
                    exp.append((e[0], e[1], e[2] + 1))
        if update:
            self.explosions = exp

    def frame(self):
        self.matrix.clear()
        for i in range(16):
            self.matrix.drawLine(i, 15, i, 15 - self.buildings[i], colors.Blue)

        if self._step % self._frames_per_missle_move == 0:
            missiles = []
            for m in self.missiles:
                if m[1] <= 15:
                    m_next = m[1] + 1
                    if m_next == 15 - self.buildings[m[0]]:
                        self.explosions.append((m[0], m_next, 1))
                    else:
                        missiles.append((m[0], m_next))
            self.missiles = missiles

            self._draw_explosions(True)
            self._draw_missiles()
        else:
            self._draw_explosions(False)
            self._draw_missiles()

        if randint(0, 30) == 0:
            self.missiles.append((randint(0, 15), -1))

        self._step += 1