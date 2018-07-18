import math
from . import colors

class Matrix(object):
    def __init__(self, pixels, coords):
        self.pixels = pixels
        self.map = coords
        self.width = len(self.map)
        self.height = None
        for col in self.map:
            y = len(col)
            if self.height is None:
                self.height = y
            else:
                if y != self.height:
                    raise ValueError('All columns of coords must be the same length!')

    def clear(self):
        self.pixels.clear()

    def set(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        i = self.map[y][x]
        self.pixels.set(i, color)

    ##########################################################################
    # Drawing Functions
    # Lovingly borrowed from Adafruit
    # https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.cpp
    ##########################################################################

    def drawCircle(self, x0, y0, r, color=None):
        """Draws a circle at point x0, y0 with radius r of the specified RGB color"""
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.set(x0, y0 + r, color)
        self.set(x0, y0 - r, color)
        self.set(x0 + r, y0, color)
        self.set(x0 - r, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            self.set(x0 + x, y0 + y, color)
            self.set(x0 - x, y0 + y, color)
            self.set(x0 + x, y0 - y, color)
            self.set(x0 - x, y0 - y, color)
            self.set(x0 + y, y0 + x, color)
            self.set(x0 - y, y0 + x, color)
            self.set(x0 + y, y0 - x, color)
            self.set(x0 - y, y0 - x, color)

    def _drawCircleHelper(self, x0, y0, r, cornername, color=None):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while x < y:
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if (cornername & 0x4):
                self.set(x0 + x, y0 + y, color)
                self.set(x0 + y, y0 + x, color)

            if (cornername & 0x2):
                self.set(x0 + x, y0 - y, color)
                self.set(x0 + y, y0 - x, color)

            if (cornername & 0x8):
                self.set(x0 - y, y0 + x, color)
                self.set(x0 - x, y0 + y, color)

            if (cornername & 0x1):
                self.set(x0 - y, y0 - x, color)
                self.set(x0 - x, y0 - y, color)

    def _fillCircleHelper(self, x0, y0, r, cornername, delta, color=None):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while (x < y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            if (cornername & 0x1):
                self._drawFastVLine(x0 + x, y0 - y, 2 * y + 1 + delta, color)
                self._drawFastVLine(x0 + y, y0 - x, 2 * x + 1 + delta, color)

            if (cornername & 0x2):
                self._drawFastVLine(x0 - x, y0 - y, 2 * y + 1 + delta, color)
                self._drawFastVLine(x0 - y, y0 - x, 2 * x + 1 + delta, color)

    def fillCircle(self, x0, y0, r, color=None):
        """Draws a filled circle at point x0,y0 with radius r and specified color"""
        self._drawFastVLine(x0, y0 - r, 2 * r + 1, color)
        self._fillCircleHelper(x0, y0, r, 3, 0, color)

    def drawLine(self, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
        if aa:
            self.wu_line(x0, y0, x1, y1, color, colorFunc)
        else:
            self.bresenham_line(x0, y0, x1, y1, color, colorFunc)

    # Bresenham's algorithm
    def bresenham_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)

        err = dx / 2

        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        count = 0
        for x in range(x0, x1 + 1):
            if colorFunc:
                color = colorFunc(count)
                count += 1

            if steep:
                self.set(y0, x, color)
            else:
                self.set(x, y0, color)

            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
    # END Bresenham's algorithm

    # Xiaolin Wu's Line Algorithm
    def wu_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        funcCount = [0]  # python2 hack since nonlocal not available

        def plot(x, y, level):
            c = color
            if colorFunc:
                c = colorFunc(funcCount[0])
                funcCount[0] += 1

            c = colors.color_scale(color, int(255 * level))
            self.set(int(x), int(y), c)

        def ipart(x):
            return int(x)

        def fpart(x):
            return x - math.floor(x)

        def rfpart(x):
            return 1.0 - fpart(x)

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx

        # handle first endpoint
        xend = round(x0)
        yend = y0 + gradient * (xend - x0)
        xgap = rfpart(x0 + 0.5)
        xpxl1 = xend  # this will be used in the main loop
        ypxl1 = ipart(yend)

        if steep:
            plot(ypxl1, xpxl1, rfpart(yend) * xgap)
            plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
        else:
            plot(xpxl1, ypxl1, rfpart(yend) * xgap)
            plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

        # first y-intersection for the main loop
        intery = yend + gradient

        # handle second endpoint
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = fpart(x1 + 0.5)
        xpxl2 = xend  # this will be used in the main loop
        ypxl2 = ipart(yend)

        if steep:
            plot(ypxl2, xpxl2, rfpart(yend) * xgap)
            plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
        else:
            plot(xpxl2, ypxl2, rfpart(yend) * xgap)
            plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

        # main loop
        for x in range(int(xpxl1 + 1), int(xpxl2)):
            if steep:
                plot(ipart(intery), x, rfpart(intery))
                plot(ipart(intery) + 1, x, fpart(intery))
            else:
                plot(x, ipart(intery), rfpart(intery))
                plot(x, ipart(intery) + 1, fpart(intery))
            intery = intery + gradient

    # END Xiaolin Wu's Line Algorithm

    def _drawFastVLine(self, x, y, h, color=None, aa=False):
        self.drawLine(x, y, x, y + h - 1, color, aa)

    def _drawFastHLine(self, x, y, w, color=None, aa=False):
        self.drawLine(x, y, x + w - 1, y, color, aa)

    def drawRect(self, x, y, w, h, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w and height h"""
        self._drawFastHLine(x, y, w, color, aa)
        self._drawFastHLine(x, y + h - 1, w, color, aa)
        self._drawFastVLine(x, y, h, color, aa)
        self._drawFastVLine(x + w - 1, y, h, color, aa)

    def fillRect(self, x, y, w, h, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w and height h"""
        for i in range(x, x + w):
            self._drawFastVLine(i, y, h, color, aa)

    def fillScreen(self, color=None):
        """Fill the matrix with the given RGB color"""
        self.fillRect(0, 0, self.width, self.height, color)

    def drawRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self._drawFastHLine(x + r, y, w - 2 * r, color, aa)  # Top
        self._drawFastHLine(x + r, y + h - 1, w - 2 * r, color, aa)  # Bottom
        self._drawFastVLine(x, y + r, h - 2 * r, color, aa)  # Left
        self._drawFastVLine(x + w - 1, y + r, h - 2 * r, color, aa)  # Right
        # draw four corners
        self._drawCircleHelper(x + r, y + r, r, 1, color, aa)
        self._drawCircleHelper(x + w - r - 1, y + r, r, 2, color, aa)
        self._drawCircleHelper(x + w - r - 1, y + h - r - 1, r, 4, color, aa)
        self._drawCircleHelper(x + r, y + h - r - 1, r, 8, color, aa)

    def fillRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self.fillRect(x + r, y, w - 2 * r, h, color, aa)
        self._fillCircleHelper(x + w - r - 1, y + r, r,
                               1, h - 2 * r - 1, color, aa)
        self._fillCircleHelper(x + r, y + r, r, 2, h - 2 * r - 1, color, aa)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
        self.drawLine(x0, y0, x1, y1, color, aa)
        self.drawLine(x1, y1, x2, y2, color, aa)
        self.drawLine(x2, y2, x0, y0, color, aa)

    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
        a = b = y = last = 0

        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        if y1 > y2:
            y2, y1 = y1, y2
            x2, x1 = x1, x2
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
            a = b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self._drawFastHLine(a, y0, b - a + 1, color, aa)

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0

        # For upper part of triangle, find scanline crossings for segments
        # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
        # is included here (and second loop will be skipped, avoiding a /0
        # error there), otherwise scanline y1 is skipped here and handled
        # in the second loop...which also avoids a /0 error here if y0=y1
        # (flat-topped triangle).

        if y1 == y2:
            last = y1  # include y1 scanline
        else:
            last = y1 - 1  # skip it

        for y in range(y, last + 1):
            a = x0 + sa / dy01
            b = x0 + sb / dy02
            sa += dx01
            sb += dx02

            if a > b:
                a, b = b, a
            self._drawFastHLine(a, y, b - a + 1, color, aa)

        # For lower part of triangle, find scanline crossings for segments
        # 0-2 and 1-2.  This loop is skipped if y1=y2.
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)

        for y in range(y, y2 + 1):
            a = x1 + sa / dy12
            b = x0 + sb / dy02
            sa += dx12
            sb += dx02

            if a > b:
                a, b = b, a
            self._drawFastHLine(a, y, b - a + 1, color, aa)




