import math

def srange(a, b, step=1):
    if a <= b:
        return range(a, b + 1, step)
    else:
        return range(b, a - 1, -1 * step)

def genVector(width, height, x_mult=1, y_mult=1):
    """Generates a map of vector lengths from the center point to each coordinate
    widht - width of matrix to generate
    height - height of matrix to generate
    x_mult - value to scale x-axis by
    y_mult - value to scale y-axis by
    """
    centerX = (width - 1) / 2.0
    centerY = (height - 1) / 2.0

    return [[int(math.sqrt(math.pow(x - centerX, 2 * x_mult) + math.pow(y - centerY, 2 * y_mult))) for x in range(width)] for y in range(height)]
