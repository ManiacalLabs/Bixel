from bixel_driver import Bixel
from pixels import Pixels
from matrix import Matrix
import colors
from time import sleep, time
import random
from coords import coords



color_map = []
for y in range(16):
    row = [colors.hue2rgb_spectrum(x + (y << 4)) for x in range(16)]
    color_map.append(row)


pixels = Pixels(256)
matrix = Matrix(pixels, coords)
bixel = Bixel(pixels)
bixel.setMasterBrightness(8)


while True:
    matrix.clear()
    bixel.getButtons()
    pressed = bixel.buttons.pressed()
    for x, y in pressed:
        matrix.set(x, y, color_map[x][y])

    if len(pressed) >= 2:
        x0, y0 = pressed[0]
        x1, y1 = pressed[1]
        matrix.drawLine(x0, y0, x1, y1, colors.Red, aa=True)

    bixel.update()
    sleep(0.04)


# for i in range(16):
#     matrix.set(i, i, (255, 0, 0))
#     bixel.update()
#     sleep(0.5)



bixel.update()

# pixels.clear()
# bixel.update()

# def print_btns():
#     # print(bixel.btns)
#     for y in range(16):
#         btns = [int(bixel.btn(x, y)) for x in range(16)]
#         print(btns)

# while True:
#     i = random.randint(0, 255)
#     pixels.clear()
#     pixels.set(i, (255, 0, 0))
#     bixel.update()

#     bixel.getButtons()
#     # print_btns()
#     pressed = bixel.btns_pressed
#     print(pressed)
#     print(bixel.btn_int_high)
#     print(bixel.btn_int_low)

#     print('\n\n')

#     sleep(0.2)

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