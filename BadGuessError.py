__author__ = 'william'


class BadGuessError(Exception):

    def __init__(self, cell_name, val, message):
        self.cell_name = cell_name
        self.val = val
        self.message = message

    def __str__(self):
        return repr(self.cell_name + " " + str(self.val) + " " + self.message)
