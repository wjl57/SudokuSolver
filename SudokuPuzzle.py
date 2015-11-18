from collections import defaultdict
import copy
from SudokuCell import SudokuCell
from SudokuHelper import all_locs
from SudokuHelper import cell_locs
from SudokuHelper import all_possibilities
import SudokuHelper

__author__ = 'william'


class SudokuPuzzle:

    def __init__(self, board):
        # A dictionary from cell name to the SudokuCell object
        self.cells_dict = {}
        # A 2d matrix containing cell names
        self.board = [[None for x in all_locs] for y in all_locs]
        # y_cell_list[n] contains a set with the names for each cell in row n
        self.y_cell_list = [set() for _ in all_locs]
        # x_cell_list[n] contains a set with the names for each cell in col n
        self.x_cell_list = [set() for _ in all_locs]
        # block_cell_list[n] contains a set with the names for each cell in block n
        self.block_cell_list = [set() for _ in all_locs]
        # remaining_in_y[n] contains the remaining values in row n
        self.remaining_in_y = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # remaining_in_x[n] contains the remaining values in col n
        self.remaining_in_x = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # remaining_in_blocks[n] contains the remaining values in block n
        self.remaining_in_blocks = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # locs_left_by_y[y][val] contains a set with all the locations of val in row y
        self.locs_left_by_y = [defaultdict(set) for y in all_locs]
        # locs_left_by_x[x][val] contains a set with all the locations of val in col x
        # self.locs_left_by_x = [defaultdict(set) for x in all_locs]
        # locs_left_by_block[b][val] contains a set with all the locations of val in block b
        # self.locs_left_by_block = [defaultdict(set) for block_num in all_locs]

        for y in all_locs:
            for x in all_locs:
                c = SudokuCell(y, x)
                self.cells_dict[c.name] = c
                self.board[y][x] = c.name
                self.y_cell_list[c.y].add(c.name)
                self.x_cell_list[c.x].add(c.name)
                self.block_cell_list[c.block].add(c.name)

        for y in all_locs:
            for x in all_locs:
                val = board[y][x]
                if val is not None:
                    self.set_val_in_puzzle(y, x, val)

        for y in all_locs:
            for x in all_locs:
                # possibilities = self.cells_dict[self.board[y][x]].possibilities
                cell = self.cells_dict[self.board[y][x]]
                possibilities = cell.possibilities
                for p in possibilities:
                    self.locs_left_by_y[cell.y][p].add(cell.x)
                    # self.locs_left_by_x[cell.x][p].add(cell.y)
                    # self.locs_left_by_block[cell.block][p].add(cell.block_cell_num)

    def set_val_in_puzzle(self, y, x, val):
        cell_name = self.board[y][x]
        c = self.cells_dict[cell_name]
        self.remaining_in_y[c.y].discard(val)
        self.remaining_in_x[c.x].discard(val)
        self.remaining_in_blocks[c.block].discard(val)
        c.set_val(val)

        for other_name in self.y_cell_list[c.y]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.x_cell_list[c.x]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.block_cell_list[c.block]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)

    def remove_possibilities_from_puzzle_by_loc(self, y, x, val):
        cell_name = self.board[y][x]
        self.remove_possibilities_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibilities_from_puzzle_by_cell_name(self, cell_name, val):
        cell = self.cells_dict[cell_name]
        cell.remove_possibilities({val})
        self.locs_left_by_y[cell.y][val].discard(cell.x)
        # self.locs_left_by_x[cell.x][val].discard(cell.y)
        # self.locs_left_by_block[cell.block][val].discard(cell.block_cell_num)

    def get_possibilities(self):
        return [[self.cells_dict[self.board[y][x]].possibilities for x in all_locs] for y in all_locs]

    def get_board(self):
        return [[self.cells_dict[self.board[y][x]].val for x in all_locs] for y in all_locs]

    def fill_sole_candidates(self):
        for y in all_locs:
            for x in all_locs:
                c = self.cells_dict[self.board[y][x]]
                if len(c.possibilities) == 1:
                    self.set_val_in_puzzle(y, x, next(iter(c.possibilities)))

    def fill_unique_candidates(self):
        for y in all_locs:
            y_possibilities = self.y_cell_list[y]

    def enumerate_row_possibilities(self, y):
        row_possibilities = []
        for x in all_locs:
            row_possibilities.append(self.cells_dict[self.board[y][x]].possibilities)
        return row_possibilities

    def enumerate_col_possibilities(self, x):
        col_possibilities = []
        for y in all_locs:
            col_possibilities.append(self.cells_dict[self.board[y][x]].possibilities)
        return col_possibilities

    def enumerate_block_possibilities(self, block_num):
        block_possibilities = []
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        for y_offset in cell_locs:
            for x_offset in cell_locs:
                p = self.cells_dict[self.board[y_block + y_offset][x_block + x_offset]].possibilities
                block_possibilities.append(p)
        return block_possibilities

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