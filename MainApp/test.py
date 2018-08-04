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
apa.setMasterBrightness(32)
btns = BixelButtonSerial()


def print_btns(btn_obj):
    for y in range(16):
        btns = [int(btn_obj.get(x, y)) for x in range(16)]
        print(btns)
    print('')


try:
    for s in range(0, 256, 16):
        pixels.clear()
        for i in range(16):
            pixels.set(s + i, colors.Red)
        apa.update()
        sleep(0.25)

    c = 0
    while True:
        btn_obj = btns.get()
        pressed = btn_obj.pressed()
        print_btns(btn_obj)
        matrix.clear()
        for x, y in pressed:
            matrix.set(x, y, colors.Red)
        # for i in range(c):
        #     pixels.set(i, colors.Red)
        apa.update()
        c += 1
        if c >= 256:
            c = 0
        sleep(0.1)
except KeyboardInterrupt:
    matrix.clear()
    apa.update()
    sleep(1)
