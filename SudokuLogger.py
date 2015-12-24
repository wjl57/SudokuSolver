from flask import jsonify
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
        count = 0
        for step in self.sudoku_log:
            print("Step " + str(count) + ":\n" + str(step))
            count += 1


class SudokuStepLog:

    def __init__(self, description, filled_cell, updated_cells, board, possibilities, additional):
        self.description = description
        self.filled_cell = filled_cell
        self.updated_cells = updated_cells
        self.board = board
        self.possibilities = possibilities
        self.additional = additional

    def __str__(self):
        s = self.description + ""
        if self.filled_cell:
            s += "\nUpdated cell: " + str(self.filled_cell)
        if self.updated_cells:
            s += "\nRemoved candidates: " + str(self.updated_cells)
        if self.additional:
            s += "\n" + str(self.additional)
        if self.board:
            s += "\n" + SudokuPuzzle.get_pretty_matrix_string(self.board)
        if not self.filled_cell and self.updated_cells:
            s += "\n" + SudokuPuzzle.get_pretty_matrix_string(self.possibilities)
        return s

    def to_json(self):
        return {
            'description': self.description,
            # 'filled_cell': self.filled_cell.serialize(),
            'updated_cells': [{'cell_name': cn, 'candidate': c} for cn, c in self.updated_cells]
            if self.updated_cells else [],
            'board': self.board,
            'possibilities': self.possibilities,
            'additional': self.additional
        }
