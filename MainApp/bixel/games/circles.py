from . base import BaseGame
from .. import colors
from random import randint


# color_map = []
# for y in range(16):
#     row = [colors.hue2rgb_spectrum(x + (y << 4)) for x in range(16)]
#     color_map.append(row)


class circles(BaseGame):
    def setup(self):
        self.circles = []

    def frame(self):
        self.matrix.clear()
        for x, y in self.buttons.int_high():
            c = colors.hue2rgb_spectrum(randint(0, 255))
            self.circles.append({'x': x, 'y': y, 'size': 1, 'c': c})

        new_list = []
        for c in self.circles:
            x = c['x']
            y = c['y']
            size = c['size']
            color = c['c']

            if (x + size < 24 or x - size >= -8) or (y + size < 24 or y - size >= -8):
                self.matrix.drawCircle(x, y, int(size), color)
                c['size'] += 0.5
                new_list.append(c)

        self.circles = new_list


