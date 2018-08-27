from . base import BaseGame
from .. import colors
from random import randint


class MissileCommand(BaseGame):
    def setup(self):
        self._tail = 4
        self._frames_per_missle_move = 15

    def reset(self):
        self.buildings = [randint(1, 4) for _ in range(16)]
        self.missiles = []
        self.explosions = []
        self._step = 0
        self._exploded_missiles = 0
        self.end_game = False

        # self.missiles.append((randint(0, 15), -5))

    def _draw_missile(self, x, y):
        self.matrix.set(x, y, colors.Red)
        for i in range(1, self._tail + 1):
            if y - i >= 0 and y - i < 16:
                level = 255 - ((255 // self._tail) * i)
                self.matrix.set(x, y - i, colors.color_scale(colors.DarkOrange, level))

    def _draw_missiles(self):
        for m in self.missiles:
            self._draw_missile(m[0], m[1])

    def _draw_explosions(self):
        exp = []
        for e in self.explosions:
            self.matrix.drawCircle(e[0], e[1], int(e[2]), e[3])
            if int(e[2]) <= 3:
                exp.append((e[0], e[1], e[2] + 0.4, e[3]))
        self.explosions = exp

    def _check_missile_press(self):
        res = []
        for m in self.missiles:
            if self.buttons.get(m[0], m[1]):
                self._exploded_missiles += 1
                self._add_explosion(m[0], m[1], colors.Fuchsia)
            else:
                res.append(m)
        self.missiles = res

    def _add_explosion(self, x, y, color):
        self.explosions.append((x, y, 1, color))

    def frame(self):
        self.matrix.clear()
        if self.end_game:
            if randint(0, 1) == 0:
                self._add_explosion(randint(0, 15), randint(0, 15), colors.Red)
            self._draw_explosions()
        else:
            if all(b == 0 for b in self.buildings):
                self.end_game = True
            else:
                for i in range(16):
                    if self.buildings[i]:
                        self.matrix.drawLine(i, 15, i, 15 - self.buildings[i] + 1, colors.Blue)

                if self._step % self._frames_per_missle_move == 0:
                    missiles = []
                    for m in self.missiles:
                        if m[1] <= 15:
                            m_next = m[1] + 1
                            if self.buildings[m[0]] and m_next == 16 - self.buildings[m[0]]:
                                self._add_explosion(m[0], m_next, colors.Green)
                                self.buildings[m[0]] -= 1
                            elif self.buildings[m[0]] == 0 and m_next == 15:
                                self._add_explosion(m[0], 15, colors.Green)
                            else:
                                missiles.append((m[0], m_next))
                    self.missiles = missiles
                    self._draw_missiles()
                else:
                    self._draw_missiles()

                self._check_missile_press()
                self._draw_explosions()

                if randint(0, int(sum(self.buildings) * 2)) <= int(0 + (self._exploded_missiles / 8)):
                    self.missiles.append((randint(0, 15), -1))

                self._step += 1