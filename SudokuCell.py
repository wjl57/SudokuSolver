import copy
import SudokuHelper
from SudokuHelper import all_possibilities

__author__ = 'william'


class SudokuCell:

    def __init__(self, y, x, possibilities=None, val=None):
        self.y = y
        self.x = x
        self.block = SudokuHelper.loc_to_block_num(y, x)
        self.block_cell_num = SudokuHelper.loc_to_block_cell_num(y, x)
        self.possibilities = copy.deepcopy(possibilities if possibilities is not None else all_possibilities)
        self.name = 'c' + str(self.y) + str(self.x) + str(self.block)
        self.val = val

    def set_val(self, val):
        self.val = val
        self.possibilities = {val}

    def remove_possibility(self, possibility):
        if possibility in self.possibilities:
            self.possibilities.discard(possibility)
            return True
        return False

    def to_json(self):
        return {
            'y': self.y,
            'x': self.x,
            'block': self.block,
            'possibilities': self.possibilities,
            'candidate': self.val,
            'name': self.name
        }


