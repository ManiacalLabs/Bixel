from . base import BaseGame
from .. import colors
from random import randint


class Tanks(BaseGame):
    def setup(self):
        self._tail = 4
        self._frames_per_missle_move = 15

    def reset(self):
        self.buildings = [randint(1, 4) for _ in range(16)]
        self.red = (0, 15 - self.buildings[0])
        self.blue = (15, 15 - self.buildings[15])
        self.turn = False
        self.explosions = []
        self._step = 0

        self._accel = -5
        self._speed = 0
        self._dir = 0
        self._round = None

    def _draw_explosions(self):
        exp = []
        for e in self.explosions:
            self.matrix.drawCircle(e[0], e[1], int(e[2]), e[3])
            if int(e[2]) <= 3:
                exp.append((e[0], e[1], e[2] + 0.4, e[3]))
        self.explosions = exp

    def _add_explosion(self, x, y, color):
        self.explosions.append((x, y, 1, color))

    def _draw_tanks(self):
        blink = self._step % 15 >= 8
        self.matrix.set(self.red[0], self.red[1], colors.White if (blink and self.turn) else colors.Red)
        self.matrix.set(self.blue[0], self.blue[1], colors.White if (blink and not self.turn) else colors.Blue)

    def frame(self):
        self.matrix.clear()

        for i in range(16):
            if self.buildings[i]:
                self.matrix.drawLine(i, 15, i, 15 - self.buildings[i] + 1, colors.Green)

            self._draw_tanks()

        btns = list(self.buttons.int_high())
        if btns:
            x, y = btns[0]
            self._round = list(self.red if self.turn else self.blue)
            self._dir = 1 if self.turn else -1
            self._speed = 10

        if self._round:
            if self._step % 10 == 0:
                self._round[0] += self._dir
            s = self._speed
            if s < 0:
                s += (self._accel + 1)
            if self._step % s == 0:
                if self._speed > 0:
                    self._round[1] -= 1
                    self._speed -= 1
                else:
                    self._round[1] += 1
                    self._speed += 1
                if self._speed == 0:
                    self._speed = -1

            self.matrix.set(self._round[0], self._round[1], colors.DarkOrange)

        self._step += 1


        # if self.end_game:
        #     if randint(0, 1) == 0:
        #         self._add_explosion(randint(0, 15), randint(0, 15), colors.Red)
        #     self._draw_explosions()
        # else:
        #     if all(b == 0 for b in self.buildings):
        #         self.end_game = True
        #     else:
        #         for i in range(16):
        #             if self.buildings[i]:
        #                 self.matrix.drawLine(i, 15, i, 15 - self.buildings[i] + 1, colors.Blue)

        #         if self._step % self._frames_per_missle_move == 0:
        #             missiles = []
        #             for m in self.missiles:
        #                 if m[1] <= 15:
        #                     m_next = m[1] + 1
        #                     if self.buildings[m[0]] and m_next == 16 - self.buildings[m[0]]:
        #                         self._add_explosion(m[0], m_next, colors.Green)
        #                         self.buildings[m[0]] -= 1
        #                     elif self.buildings[m[0]] == 0 and m_next == 15:
        #                         self._add_explosion(m[0], 15, colors.Green)
        #                     else:
        #                         missiles.append((m[0], m_next))
        #             self.missiles = missiles
        #             self._draw_missiles()
        #         else:
        #             self._draw_missiles()

        #         self._check_missile_press()
        #         self._draw_explosions()

        #         if randint(0, int(sum(self.buildings) * 2)) <= int(0 + (self._exploded_missiles / 8)):
        #             self.missiles.append((randint(0, 15), -1))

        #         self._step += 1