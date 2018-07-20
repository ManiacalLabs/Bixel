from bixel_driver import Bixel
from pixels import Pixels
from matrix import Matrix
from runner import BixelRunner
from coords import coords
import circles
import lightbrite

pixels = Pixels(256)
matrix = Matrix(pixels, coords)
bixel = Bixel(pixels)
bixel.setMasterBrightness(8)

# runner = BixelRunner(bixel, matrix, circles.circles)
runner = BixelRunner(bixel, matrix, lightbrite.lightbrite)

runner.start()