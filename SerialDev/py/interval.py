import time

class IntervalRunner(object):
    def __init__(self, run_method, delay_ms, args = ()):
        self.run = run_method
        self.delay = delay_ms / 1000.0
        self.args = args

    def start(self):
        while True:
            start = time.monotonic()
            self.run(*self.args)
            delta = time.monotonic() - start
            if delta < self.delay:
                time.sleep(self.delay - delta)
            else:
                print('Frame required {} ms'.format(int(delta * 1000)))

