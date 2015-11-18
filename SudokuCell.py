import SudokuHelper

__author__ = 'william'


class SudokuCell:

    y = -1
    x = -1
    block = -1
    block_cell_num = -1
    possibilities = set()
    val = None
    name = ''

    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.block = SudokuHelper.loc_to_block_num(y, x)
        self.block_cell_num = SudokuHelper.loc_to_block_cell_num(y, x)
        self.possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.name = 'c' + str(self.y) + str(self.x) + str(self.block)

    def set_val(self, val):
        self.val = val
        self.possibilities = set()

    def remove_possibilities(self, possibilities):
        self.possibilities.difference_update(possibilities)


