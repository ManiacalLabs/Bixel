from bixel_driver import Bixel
from pixels import Pixels
from time import sleep

pixels = Pixels(256)
bixel = Bixel(pixels)

for i in range(24):
    pixels.set(i, (255, 0, 0))
    bixel.update()
    sleep(0.05)

pixels.clear()
bixel.update()