import matrix_drawing as md


class Matrix(object):
    def __init__(self, pixels, coords):
        self.pixels = pixels
        self.map = coords
        self.width = len(self.map)
        self.height = None
        for col in self.map:
            y = len(col)
            if self.height is None:
                self.height = y
            else:
                if y != self.height:
                    raise ValueError('All columns of coords must be the same length!')

    def clear(self):
        self.pixels.clear()

    def set(self, x, y, color):
        if x >= self.width or y >= self.height:
            return
        i = self.map[x][y]
        self.pixels.set(i, color)




