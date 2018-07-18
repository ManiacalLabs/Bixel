from . base import BaseGame
from .. import colors


color_map = []
for y in range(16):
    row = [colors.hue2rgb_spectrum(x + (y << 4)) for x in range(16)]
    color_map.append(row)


class circles(BaseGame):
    def setup(self):
        self.circles = []

    def frame(self):
        self.matrix.clear()
        for x, y in self.buttons.int_high():
            self.circles.append({'x': x, 'y': y, 'size': 1})

        new_list = []
        for c in self.circles:
            x = c['x']
            y = c['y']
            size = c['size']

            if (x + size < 24 or x - size >= -8) or (y + size < 24 or y - size >= -8):
                self.matrix.drawCircle(x, y, int(size), color_map[x][y])
                c['size'] += 0.5
                new_list.append(c)

        self.circles = new_list


