from bixel_driver import Bixel
from pixels import Pixels

pixels = Pixels(256)
bixel = Bixel(pixels)

pixels.set(0, (0, 0, 0))
bixel.update()