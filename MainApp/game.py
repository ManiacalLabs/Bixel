from bixel.runner import BixelRunner
from bixel.APA102 import APA102
from bixel.pixels import Pixels
from bixel.matrix import Matrix
from bixel.coords import coords
from bixel.serial_btns import BixelButtonSerial

# games
from bixel.games import circles
from bixel.games import lightbrite
from bixel.games import GameOfLife

pixels = Pixels(256)
matrix = Matrix(pixels, coords)
apa = APA102(pixels)
apa.setMasterBrightness(8)
btns = BixelButtonSerial()

runner = BixelRunner(btns, apa, matrix)
runner.add_game(circles.circles)
runner.add_game(lightbrite.lightbright)
runner.add_game(GameOfLife.GameOfLife, kwargs={'frames_per_step': 15})

runner.select_game(2)

runner.start()