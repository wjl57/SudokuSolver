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
        # A 2D-matrix containing cell names
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
        self.locs_left_by_x = [defaultdict(set) for x in all_locs]
        # locs_left_by_block[b][val] contains a set with all the locations of val in block b
        self.locs_left_by_block = [defaultdict(set) for block_num in all_locs]

        # For every location create a SudokuCell object and add it to the appropriate cell lists
        for y in all_locs:
            for x in all_locs:
                c = SudokuCell(y, x)
                self.cells_dict[c.name] = c
                self.board[y][x] = c.name
                self.y_cell_list[c.y].add(c.name)
                self.x_cell_list[c.x].add(c.name)
                self.block_cell_list[c.block].add(c.name)

        # Set all the known values
        for y in all_locs:
            for x in all_locs:
                val = board[y][x]
                if val is not None:
                    self.set_val_in_puzzle(y, x, val)

        # Initialize all locs_left_by according to the remaining possibilities
        for cell_name in self.cells_dict.keys():
            cell = self.cells_dict[cell_name]
            possibilities = cell.possibilities
            for p in possibilities:
                self.locs_left_by_y[cell.y][p].add(cell.x)
                self.locs_left_by_x[cell.x][p].add(cell.y)
                self.locs_left_by_block[cell.block][p].add(cell.block_cell_num)

    def set_val_in_puzzle(self, y, x, val):
        """
        Sets the cell at position (y,x) to the val.
        Removes possibilities from remaining_in and locs_left_by fields
        :param y: The y location of the cell. Precondition: 0 <= y < 9
        :param x: The x location of the cell. Precondition: 0 <= x < 9
        :param val: The value to set. Precondition: 1 <= val <= 9
        """
        cell_name = self.board[y][x]
        c = self.cells_dict[cell_name]
        self.remaining_in_y[c.y].discard(val)
        self.remaining_in_x[c.x].discard(val)
        self.remaining_in_blocks[c.block].discard(val)
        c.set_val(val)

        # Remove possibilities from row, col, block
        for other_name in self.y_cell_list[c.y]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.x_cell_list[c.x]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.block_cell_list[c.block]:
            self.remove_possibilities_from_puzzle_by_cell_name(other_name, val)

    def remove_possibilities_from_puzzle_by_loc(self, y, x, val):
        """
        Removes the val from the cell at position (y,x)'s possibilities.
        Also removes the val from the locs_left_by dicts
        :param y: The y location of the cell. Precondition: 0 <= y < 9
        :param x: The x location of the cell. Precondition: 0 <= x < 9
        :param val: The value to remove. Precondition: 1 <= val <= 9
        """
        cell_name = self.board[y][x]
        self.remove_possibilities_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibilities_from_puzzle_by_cell_name(self, cell_name, val):
        """
        Removes the val from the cell's possibilities.
        Also removes the val from the locs_left_by dicts
        :param cell_name: The name of the cell
        :param val: The value to remove. Precondition: 1 <= val <= 9
        """
        cell = self.cells_dict[cell_name]
        cell.remove_possibilities({val})
        self.locs_left_by_y[cell.y][val].discard(cell.x)
        self.locs_left_by_x[cell.x][val].discard(cell.y)
        self.locs_left_by_block[cell.block][val].discard(cell.block_cell_num)

    def get_possibilities(self):
        """
        :return: A 2D-matrix of possibilities for the puzzle
        """
        return [[self.cells_dict[self.board[y][x]].possibilities for x in all_locs] for y in all_locs]

    def get_board(self):
        """
        :return: A 2D-matrix of filled in values for the puzzle
        """
        return [[self.cells_dict[self.board[y][x]].val for x in all_locs] for y in all_locs]

    def fill_sole_candidates(self):
        """
        Fills in sole candidates
        i.e. when a specific cell can only contain a single number
        """
        for cell_name in self.cells_dict.keys():
            cell = self.cells_dict[cell_name]
            if len(cell.possibilities) == 1:
                self.set_val_in_puzzle(cell.y, cell.x, next(iter(cell.possibilities)))

    def fill_unique_candidates_y(self, y):
        """
        Fills in unique candidates by row
        i.e. when a number can only go in one spot in row y
        :param y: The row number
        """
        y_locs_left = self.locs_left_by_y[y]
        y_possibilities = self.remaining_in_y[y]
        for val in copy.deepcopy(y_possibilities):
            if len(y_locs_left[val]) == 1:
                self.set_val_in_puzzle(y, next(iter(y_locs_left[val])), val)

    def fill_unique_candidates_x(self, x):
        """
        Fills in unique candidates by col
        i.e. when a number can only go in one spot in col x
        :param x: The col number
        """
        x_locs_left = self.locs_left_by_x[x]
        x_possibilities = self.remaining_in_x[x]
        for val in copy.deepcopy(x_possibilities):
            if len(x_locs_left[val]) == 1:
                self.set_val_in_puzzle(next(iter(x_locs_left[val])), x, val)

    def fill_unique_candidates_block(self, block_num):
        """
        Fills in unique candidates by block
        i.e. when a number can only go in one spot in block block_number
        :param block_num: The block number
        """
        block_locs_left = self.locs_left_by_block[block_num]
        block_possibilities = self.remaining_in_blocks[block_num]
        for val in copy.deepcopy(block_possibilities):
            if len(block_locs_left[val]) == 1:
                (y, x) = SudokuHelper.block_num_and_cell_num_to_offsets(
                    block_num, next(iter(block_locs_left[block_num])))
                self.set_val_in_puzzle(y, x, val)

    def fill_unique_candidates(self):
        """
        Fills in unique candidates
        i.e. when a number can only go in one spot in a row/col/block
        """
        for y in all_locs:
            self.fill_unique_candidates_y(y)
        for x in all_locs:
            self.fill_unique_candidates_x(x)
        for block_num in all_locs:
            self.fill_unique_candidates_block(block_num)

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

    @staticmethod
    def rotate_board_cw(board, n=1):
        def rotate_cw(board):
            rotated_board = [[None for _ in all_locs] for _ in all_locs]
            for y in all_locs:
                for x in all_locs:
                    rotated_board[y][x] = board[8-x][y]
            return rotated_board

        for _ in range(0, n % 4):
            board = rotate_cw(board)
        return board

    @staticmethod
    def rotate_board_ccw(board, n=1):
        def rotate_ccw(board):
            rotated_board = [[None for _ in all_locs] for _ in all_locs]
            for y in all_locs:
                for x in all_locs:
                    rotated_board[y][x] = board[x][8-y]
            return rotated_board

        for _ in range(0, n % 4):
            board = rotate_ccw(board)
        return board

    @staticmethod
    def reflect_board_over_xy(board):
        rotated_board = [[None for _ in all_locs] for _ in all_locs]
        for y in all_locs:
            for x in all_locs:
                rotated_board[y][x] = board[x][y]
        return rotated_board
