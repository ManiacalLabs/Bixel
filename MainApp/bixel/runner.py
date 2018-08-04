from . interval import IntervalRunner
from gpiozero import Button
from . games.GameMenu import GameMenu


BRIGHT_LEVELS = [15, 39, 63, 87] #, 111, 135, 159, 183, 207, 231, 255]


class BixelRunner(object):
    def __init__(self, buttons, driver, matrix, delay=33, default_bright=0):
        self.buttons = buttons
        self.driver = driver
        self.matrix = matrix
        self.delay = delay
        self.brightness = default_bright

        self.games = []
        self.game_id = 0

        self.set_brightness(self.brightness)

        self.interval = IntervalRunner(self._run, self.delay)

        self.btn_bright = Button(16, bounce_time=0.01)
        self.btn_bright.when_pressed = self.brightness_pressed

        self.btn_menu = Button(20, bounce_time=0.01)
        self.btn_menu.when_pressed = self.show_menu

        self.in_menu = False

    # def init_menu(self):
    #     self.add_game(GameMenu, args=(len(self.games),))

    def show_menu(self):
        print('MENU')

    def set_brightness(self, val):
        if val >= len(BRIGHT_LEVELS):
            print('Invalid Value')
        else:
            self.driver.setMasterBrightness(BRIGHT_LEVELS[val])

    def brightness_pressed(self):
        self.brightness += 1
        if self.brightness >= len(BRIGHT_LEVELS):
            self.brightness = 0
        self.set_brightness(self.brightness)

    def add_game(self, game_class, args=(), kwargs={}):
        g = game_class(self.buttons.buttons, self.matrix)
        g.setup(*args, **kwargs)
        g.reset()
        self.games.append(g)
        return len(self.games) - 1

    def select_game(self, index):
        if index >= 0 and index < len(self.games):
            self.game_id = index
            self.games[self.game_id].reset()

    def start(self):
        if self.games:
            self.interval.start()

    def stop(self):
        self.btn_bright.close()

    def _run(self):
        self.buttons.get()
        self.games[self.game_id].frame()
        self.driver.update()
