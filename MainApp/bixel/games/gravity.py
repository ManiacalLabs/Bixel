from . base import BaseGame
from random import randint, choice
from .. import colors


class gravity(BaseGame):
    def reset(self, blocks=1):
        self._tail = 4
        self.drops = []
        self.targets = [True for _ in range(16)]
        self.blocks = []
        ys = []

        if blocks > 8:
            blocks = 8
        for _ in range(blocks):
            while True:
                y = randint(4, 14)
                if not y in ys:
                    break
            x = randint(2, 13)
            d = choice([-1, 1])
            self.blocks.append((x, y, d))
        self.explosions = []
        self._step = 0

    def _draw_explosions(self):
        exp = []
        for e in self.explosions:
            self.matrix.drawCircle(e[0], e[1], int(e[2]), e[3])
            if int(e[2]) <= 3:
                exp.append((e[0], e[1], e[2] + 0.4, e[3]))
        self.explosions = exp

    def _add_explosion(self, x, y, color):
        self.explosions.append((x, y, 1, color))

    def _drawDrop(self, x, y):
        c = colors.hue2rgb((y if y < self.matrix.height else (
            self.matrix.height - 1)) * (255 // self.matrix.height))
        for i in range(self._tail):
            if y - i >= 0 and y - i < self.matrix.height:
                level = 255 - ((255 // self._tail) * i)
                self.matrix.set(x, y - i, colors.color_scale(c, level))

    def _drawBlock(self, x, y):
        c = colors.hue_helper(x, 14, x)
        for i in range(x - 1, x + 2, 1):
            self.matrix.set(i, y, c)

    def _check_blocked(self, dx, dy):
        result = False
        _blocks = []
        for i in range(len(self.blocks)):
            x, y, d = self.blocks[i]
            if dy in [y - i for i in range(self._tail)] and dx in (x - 1, x, x + 1):
                result = True

            _blocks.append((x, y, d))

        self.blocks = _blocks

        return result

    def _check_win(self):
        if not any(self.targets):
            self.reset(blocks = len(self.blocks) + 1)

    def frame(self):
        self.matrix.clear()

        for x, y in self.buttons.int_high():
            if y == 0:
                self.drops.append((x, y))

        for i in range(len(self.targets)):
            t = self.targets[i]
            if t:
                c = colors.hue_helper(i, 16, self._step)
                self.matrix.set(i, 15, c)

        _blocks = []
        for i in range(len(self.blocks)):
            x, y, d = self.blocks[i]
            self._drawBlock(x, y)

            if self._step % 3 == 0:
                if d == 1 and x == 14:
                    d = -1
                elif d == -1 and x == 1:
                    d = 1
                move = d
            else:
                move = 0
            _blocks.append((x + move, y, d))

        self.blocks = _blocks

        _drops = []
        for x, y in self.drops:
            self._drawDrop(x, y)

            if self._check_blocked(x, y):
                self._add_explosion(x, y, colors.White)
            elif y - self._tail < 15:
                move =  1 if self._step % 3 == 0 else 0
                move *= (1 + (y / 8))
                move = int(round(move))
                _drops.append((x, y + move))
            elif y >= 15:
                self._add_explosion(x, 15, colors.Red)
                self.targets[x] = False

        self._draw_explosions()

        self.drops = _drops

        self._check_win()

        self._step += 1
