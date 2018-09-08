from . base import BaseGame
from .. import colors
from random import randint
import inspect

from noise import snoise3 as noise3
from .. util import genVector
from .. import font

class demo(BaseGame):
    def setup(self):
        self.funcs = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('func_'):
                self.funcs.append(method)

        self.cur_func = randint(0, len(self.funcs) - 1)
        # print(self.funcs)

        # func_noise
        self._freq = float(16)
        self._octaves = 1
        # func_bloom
        self._vector = genVector(self.width, self.height)
        # func_pinwheel
        self._center = (self.width // 2, self.height // 2)
        self._len = (self.width * 2) + (self.height * 2) - 2
        # _func_text_base
        self.xPos = self.width
        self.orig_xPos = self.xPos
        self.yPos = 1
        self.font_name = '8x6'
        self.font_scale = 2

    def reset(self):
        self._step = 0

    def func_noise(self):
        step = self._step / 4
        for y in range(self.height):
            for x in range(self.width):
                v = int(noise3(x / self._freq,
                               y / self._freq, step / self._freq,
                               octaves=self._octaves) * 127.0 + 128.0)
                c = colors.hue2rgb(v)
                self.matrix.set(x, y, c)

    def func_bloom(self):
        s = 255 - ((self._step * 3) % 255)

        for y in range(self.height):
            for x in range(self.width):
                c = colors.hue_helper(self._vector[y][x], self.height, s)
                self.matrix.set(x, y, c)

    def func_pinwheel(self):
        s = 255 - ((self._step * 3) % 255)

        pos = 0
        cX, cY = self._center
        for x in range(self.width):
            c = colors.hue_helper(pos, self._len, s)
            self.matrix.drawLine(cX, cY, x, 0, c)
            pos += 1

        for y in range(self.height):
            c = colors.hue_helper(pos, self._len, s)
            self.matrix.drawLine(cX, cY, self.width - 1, y, c)
            pos += 1

        for x in range(self.width - 1, -1, -1):
            c = colors.hue_helper(pos, self._len, s)
            self.matrix.drawLine(cX, cY, x, self.height - 1, c)
            pos += 1

        for y in range(self.height - 1, -1, -1):
            c = colors.hue_helper(pos, self._len, s)
            self.matrix.drawLine(cX, cY, 0, y, c)
            pos += 1

    def _func_text_base(self, text, color):
        self.matrix.drawText(text, self.xPos, self.yPos,
                             color=color, bg=colors.Off, font=self.font_name, font_scale=self.font_scale)
        if self._step % 2 == 0:
            self.xPos -= 1
        if self.xPos + self._strW <= 0:
            self.xPos = self.width - 1

    def func_text_sparkcon(self):
        text = 'SPARKCON!!'
        self._strW = font.str_dim(text, self.font_name, self.font_scale, True)[0]
        self._func_text_base(text, colors.Red)

    def func_text_ml(self):
        text = 'MANIACAL LABS'
        self._strW = font.str_dim(text, self.font_name, self.font_scale, True)[0]
        self._func_text_base(text, colors.DarkOrange)

    def frame(self):
        self.matrix.clear()
        self.funcs[self.cur_func]()
        self._step += 1
        if self._step >= 300:
            self._step = 0
            self.cur_func = randint(0, len(self.funcs) - 1)
