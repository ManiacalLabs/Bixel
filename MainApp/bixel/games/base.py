class BaseGame(object):
    def __init__(self, buttons, matrix):
        self.buttons = buttons
        self.matrix = matrix
        self.width = self.matrix.width
        self.height = self.matrix.height

    def setup(self):
        pass  # only needed if game requires init

    def reset(self):
        pass  # override if need to be able to reset