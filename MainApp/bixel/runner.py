from . interval import IntervalRunner

class BixelRunner(object):
    def __init__(self, buttons, driver, matrix, func, data = {}, args=(), delay=33):
        if not isinstance(args, tuple):
            raise ValueError('args must be a tuple')
        self.buttons = buttons
        self.driver = driver
        self.matrix = matrix
        self.func = func
        self.data = data
        self.args = (self.matrix, self.buttons.buttons, self.data) + args
        self.delay = delay

        self.interval = IntervalRunner(self._run, self.delay)

    def start(self):
        self.interval.start()

    def _run(self):
        self.buttons.get()
        self.func(*self.args)
        self.driver.update()
