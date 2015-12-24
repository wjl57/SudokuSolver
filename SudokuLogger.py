import json
from SudokuPuzzle import SudokuPuzzle

__author__ = 'william'


class SudokuLogger:

    def __init__(self):
        self.sudoku_log = []
        self.step_num = 0

    def log_step(self, description, filled_cell, updated_cells, board, possibilities, additional=None):
        if filled_cell or updated_cells or additional:
            self.sudoku_log.append(SudokuStepLog(self.step_num, description, filled_cell, updated_cells,
                                                 board, possibilities, additional))
            self.step_num += 1

    def print_log(self):
        count = 0
        for step in self.sudoku_log:
            print("Step " + str(count) + ":\n" + str(step))
            count += 1


class SudokuStepLog:

    def __init__(self, step_num, description, filled_cell, updated_cells, board, possibilities, additional):
        self.step_num = step_num
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
            'step_num': self.step_num,
            'description': self.description,
            # 'filled_cell': self.filled_cell.serialize(),
            'updated_cells': [{'cell_name': cn, 'candidate': c} for cn, c in self.updated_cells]
            if self.updated_cells else [],
            'board': json.dumps(self.board),
            'possibilities': json.dumps([[list(ps) for ps in row] for row in self.possibilities]),
            'additional': self.additional
        }
