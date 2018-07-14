from bixel_driver import Bixel
from pixels import Pixels
from time import sleep
import random

pixels = Pixels(256)
bixel = Bixel(pixels)

def print_btns():
    for y in range(16):
        btns = [int(bixel.btn(x, y)) for x in range(16)]
        print(btns)

while True:
    i = random.randint(0, 255)
    pixels.clear()
    pixels.set(i, (255, 0, 0))
    bixel.update()

    bixel.getButtons()
    print_btns()
    print('\n\n')

    sleep(0.04)

# for i in range(24):
#     pixels.set(i, (255, 0, 0))
#     bixel.update()
#     sleep(0.02)

# btns = bixel.getButtons()
# print(btns)

# pixels.clear()
# bixel.update()

# for i in range(24):
#     pixels.set(i, (255, 0, 0))
#     bixel.update()
#     sleep(0.02)

# pixels.clear()
# bixel.update()