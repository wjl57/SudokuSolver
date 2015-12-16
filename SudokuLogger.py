from SudokuPuzzle import SudokuPuzzle

__author__ = 'william'


class SudokuLogger:

    def __init__(self):
        self.sudoku_log = []

    def log_step(self, description, filled_cell, updated_cells, board, possibilities, additional=None):
        if filled_cell or updated_cells or additional:
            self.sudoku_log.append(SudokuStepLog(description, filled_cell, updated_cells,
                                                 board, possibilities, additional))

    def print_log(self):
        for step in self.sudoku_log:
            print(step)


class SudokuStepLog:

    def __init__(self, description, filled_cell, updated_cells, board, possibilities, additional):
        self.description = description
        self.filled_cell = filled_cell
        self.updated_cells = updated_cells
        self.board = board
        self.possibilities = possibilities
        self.additional = additional

    def __str__(self):
        s = self.description + ": "
        if self.filled_cell:
            s += str(self.filled_cell)
        if self.updated_cells:
            s += "\nRemoved possibilities: " + str(self.updated_cells)
        if self.additional:
            s += "\n" + str(self.additional)
        if self.board:
            s += "\n" + SudokuPuzzle.get_pretty_matrix_string(self.board)
        return s
