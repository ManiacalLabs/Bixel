from . interval import IntervalRunner

class BixelRunner(object):
    def __init__(self, buttons, driver, matrix, delay=33):
        self.buttons = buttons
        self.driver = driver
        self.matrix = matrix
        self.delay = delay

        self.games = []
        self.game_id = 0

        self.interval = IntervalRunner(self._run, self.delay)

    def add_game(self, game_class, args = (), kwargs = {}):
        g = game_class(self.buttons.buttons, self.matrix)
        g.setup(*args, **kwargs)
        g.reset
        self.games.append(g)
        return len(self.games) - 1

    def select_game(self, index):
        if index >= 0 and index < len(self.games):
            self.game_id = index
            self.games[self.game_id].reset()

    def start(self):
        if self.games:
            self.interval.start()

    def _run(self):
        self.buttons.get()
        self.games[self.game_id].frame()
        self.driver.update()
