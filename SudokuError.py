__author__ = 'william'


class BadGuessError(Exception):

    def __init__(self, cell_name, val, message):
        self.cell_name = cell_name
        self.val = val
        self.message = message

    def __str__(self):
        return "Bad Guess Because...\nCell: " + self.cell_name + "\nCandidate: " + str(self.val) + "\nReason: " + \
               self.message


class BadPuzzleError(Exception):

    def __init__(self, illegal_cells):
        self.illegal_cells = illegal_cells

    def __str__(self):
        return "Bad Puzzle because " + self.illegal_cells + " all break at least one of the Sudoku rules."
