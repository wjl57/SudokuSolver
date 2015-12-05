import copy
import SudokuHelper

__author__ = 'william'


class SudokuCell:

    def __init__(self, y, x, possibilities=None, val=None):
        self.y = y
        self.x = x
        self.block = SudokuHelper.loc_to_block_num(y, x)
        self.block_cell_num = SudokuHelper.loc_to_block_cell_num(y, x)
        self.possibilities = copy.deepcopy(possibilities) if possibilities else {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.name = 'c' + str(self.y) + str(self.x) + str(self.block)
        self.val = val if val else None

    def set_val(self, val):
        self.val = val
        self.possibilities = set()

    def remove_possibility(self, possibilities):
        self.possibilities.discard(possibilities)


