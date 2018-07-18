from bixel.runner import BixelRunner
from bixel.APA102 import APA102
from bixel.pixels import Pixels
from bixel.matrix import Matrix
from bixel.coords import coords
from bixel.serial_btns import BixelButtonSerial

# games
from bixel.games import circles
from bixel.games import lightbrite

pixels = Pixels(256)
matrix = Matrix(pixels, coords)
apa = APA102(pixels)
apa.setMasterBrightness(8)
btns = BixelButtonSerial()

runner = BixelRunner(btns, apa, matrix, circles.circles)
# runner = BixelRunner(btns, apa, matrix, lightbrite.lightbrite)

runner.start()