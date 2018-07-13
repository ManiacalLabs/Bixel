class Pixels(object):
    def __init__(self, num):
        self.numLEDs = num
        self.buffer = None

        self.clear()

    def clear(self):
        self.buffer = [0] * (3 * self.numLEDs)

    def set(self, pixel, color):
        self.buffer[pixel * 3:(pixel * 3) + 3] = color

    def setRGB(self, pixel, r, g, b):
        self.set(pixel, (r, g, b))
