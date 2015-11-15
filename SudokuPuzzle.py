import copy
from SudokuCell import SudokuCell

__author__ = 'william'

all_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
all_locs = [i for i in range(0, 9)]


class SudokuPuzzle:

    cells_dict = {}
    board = [[None for x in all_locs] for y in all_locs]
    y_dict = [set() for _ in all_locs]
    x_dict = [set() for _ in all_locs]
    block_dict = [set() for _ in all_locs]
    remaining_in_y = [copy.deepcopy(all_possibilities) for _ in all_locs]
    remaining_in_x = [copy.deepcopy(all_possibilities) for _ in all_locs]
    remaining_in_blocks = [copy.deepcopy(all_possibilities) for _ in all_locs]

    def __init__(self, board):
        for y in all_locs:
            for x in all_locs:
                c = SudokuCell(y, x)
                self.cells_dict[c.name] = c
                self.board[y][x] = c.name
                self.y_dict[c.y].add(c.name)
                self.x_dict[c.x].add(c.name)
                self.block_dict[c.block].add(c.name)

        for y in all_locs:
            for x in all_locs:
                val = board[y][x]
                if val is not None:
                    self.set_val_in_puzzle(y, x, val)

    def set_val_in_puzzle(self, y, x, val):
        cell_name = self.board[y][x]
        c = self.cells_dict[cell_name]
        self.remaining_in_y[c.y].discard(val)
        self.remaining_in_x[c.x].discard(val)
        self.remaining_in_blocks[c.block].discard(val)
        c.set_val(val)

        for other_name in self.y_dict[c.y]:
            self.cells_dict[other_name].remove_possibilities({val})
        for other_name in self.x_dict[c.x]:
            self.cells_dict[other_name].remove_possibilities({val})
        for other_name in self.block_dict[c.block]:
            self.cells_dict[other_name].remove_possibilities({val})

    def get_possibilities(self):
        return [[self.cells_dict[self.board[y][x]].possibilities for x in all_locs] for y in all_locs]

    def get_board(self):
        return [[self.cells_dict[self.board[y][x]].val for x in all_locs] for y in all_locs]

    def print_board(self):
        row_count = 0
        col_count = 0
        for y in all_locs:
            if row_count % 3 == 0:
                row_count = 0
                print('+-----------------------------+')
            row_count += 1
            for x in all_locs:
                val = self.cells_dict[self.board[y][x]].val
                if col_count % 3 == 0:
                    col_count = 0
                    print('|', end='')
                col_count += 1
                if val is None:
                    print('   ', end='')
                else:
                    print(' ' + str(val) + ' ', end='')
            print('|\n')
        print('+-----------------------------+')

    def print_possibilities(self):
        row_count = 0
        col_count = 0
        for y in all_locs:
            if row_count % 3 == 0:
                row_count = 0
                print('+-------------------------------------------------------------------+')
            row_count += 1
            for x in all_locs:
                possibilities = self.cells_dict[self.board[y][x]].possibilities
                if col_count % 3 == 0:
                    col_count = 0
                    print('|', end='')
                col_count += 1
                print(' ' + str(possibilities) + ' ', end='')
            print('|\n')
        print('+-------------------------------------------------------------------+')