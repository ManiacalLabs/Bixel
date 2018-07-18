from time import sleep
from bixel.APA102 import APA102
from bixel.pixels import Pixels
from bixel.matrix import Matrix
from bixel.coords import coords
from bixel import colors
from bixel.serial_btns import BixelButtonSerial

pixels = Pixels(256)
matrix = Matrix(pixels, coords)
apa = APA102(pixels)
apa.setMasterBrightness(8)
btns = BixelButtonSerial()

c = 0
while True:
    btn_data = btns.get()
    print(btn_data)
    pixels.set(c, colors.Red)
    c += 1
    if c >= 256:
        c = 0
    sleep(0.5)