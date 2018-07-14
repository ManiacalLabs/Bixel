from interval import IntervalRunner

class BixelRunner(object):
    def __init__(self, bixel, matrix, func, data = {}, args=(), delay=33):
        if not isinstance(args, tuple):
            raise ValueError('args must be a tuple')
        self.bixel = bixel
        self.matrix = matrix
        self.func = func
        self.data = data
        self.args = (self.matrix, self.bixel.buttons, self.data) + args
        self.delay = delay

        self.interval = IntervalRunner(self._run, self.delay)

    def start(self):
        self.interval.start()

    def _run(self):
        self.bixel.getButtons()
        self.func(*self.args)
        self.bixel.update()
