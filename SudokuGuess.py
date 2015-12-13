from SudokuCell import SudokuCell

__author__ = 'william'


class SudokuGuess:

    def __init__(self, candidate, cell_name, cells_dict, previous_guess, num_filled):
        # guess_cell_name contains the cell_name of the guess
        self.guess_cell_name = cell_name
        # guess_candidate contains the assumed candidate
        self.guess_candidate = candidate
        # previous_cells_dict contains a copy of the cells_dict before a guess was made
        self.previous_cells_dict = {}
        for cell_name, cell in cells_dict.items():
            c = SudokuCell(cell.y, cell.x, cell.possibilities, cell.val)
            self.previous_cells_dict[cell.name] = c
        # previous_guess contains the guess made before this one
        self.previous_guess = previous_guess
        # The number of cells filled before the guess
        self.num_filled = num_filled
