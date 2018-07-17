from bixel import log
from time import sleep
from bixel.serial_btns import BixelButtons, BixelButtonSerial


bixel_btns = BixelButtonSerial()


def print_btns(btn_obj):
    for y in range(16):
        btns = [int(btn_obj.get(x, y)) for x in range(16)]
        print(btns)

while True:
    btns = bixel_btns.get()
    print_btns(btns)
    print('')
    # print(btns.pressed())
    sleep(0.03)
