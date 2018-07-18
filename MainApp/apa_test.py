from time import sleep
from bixel.APA102 import APA102
from bixel.pixels import Pixels
from bixel.matrix import Matrix
from bixel.coords import coords
from bixel import colors

pixels = Pixels(256)
matrix = Matrix(pixels, coords)
apa = APA102(pixels)
apa.setMasterBrightness(32)

color_list = [colors.Red, colors.Green, colors.Blue, colors.White]

c = 0
while True:
    matrix.clear()
    matrix.drawLine(0, 0, 8, 0, color_list[c])
    apa.update()
    c += 1
    if c >= len(color_list):
        c = 0
    sleep(0.5)