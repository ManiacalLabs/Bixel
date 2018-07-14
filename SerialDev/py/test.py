from bixel_driver import Bixel
from pixels import Pixels
from matrix import Matrix, md
import colors
from time import sleep, time
import random

coords = [
    [0, 1, 2, 3, 4, 5, 6, 7, 128, 129, 130, 131, 132, 133, 134, 135],
    [15, 14, 13, 12, 11, 10, 9, 8, 143, 142, 141, 140, 139, 138, 137, 136],
    [16, 17, 18, 19, 20, 21, 22, 23, 144, 145, 146, 147, 148, 149, 150, 151],
    [31, 30, 29, 28, 27, 26, 25, 24, 159, 158, 157, 156, 155, 154, 153, 152],
    [32, 33, 34, 35, 36, 37, 38, 39, 160, 161, 162, 163, 164, 165, 166, 167],
    [47, 46, 45, 44, 43, 42, 41, 40, 175, 174, 173, 172, 171, 170, 169, 168],
    [48, 49, 50, 51, 52, 53, 54, 55, 176, 177, 178, 179, 180, 181, 182, 183],
    [63, 62, 61, 60, 59, 58, 57, 56, 191, 190, 189, 188, 187, 186, 185, 184],
    [64, 65, 66, 67, 68, 69, 70, 71, 192, 193, 194, 195, 196, 197, 198, 199],
    [79, 78, 77, 76, 75, 74, 73, 72, 207, 206, 205, 204, 203, 202, 201, 200],
    [80, 81, 82, 83, 84, 85, 86, 87, 208, 209, 210, 211, 212, 213, 214, 215],
    [95, 94, 93, 92, 91, 90, 89, 88, 223, 222, 221, 220, 219, 218, 217, 216],
    [96, 97, 98, 99, 100, 101, 102, 103, 224, 225, 226, 227, 228, 229, 230, 231],
    [111, 110, 109, 108, 107, 106, 105, 104, 239, 238, 237, 236, 235, 234, 233, 232],
    [112, 113, 114, 115, 116, 117, 118, 119, 240, 241, 242, 243, 244, 245, 246, 247],
    [127, 126, 125, 124, 123, 122, 121, 120, 255, 254, 253, 252, 251, 250, 249, 248]
]


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
    pressed = bixel.btns_pressed()
    for x, y in pressed:
        matrix.set(x, y, color_map[x][y])

    if len(pressed) >= 2:
        x0, y0 = pressed[0]
        x1, y1 = pressed[1]
        md.draw_line(matrix.set, x0, y0, x1, y1, colors.Red, aa=True)

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