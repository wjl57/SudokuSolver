from collections import defaultdict
import copy
import itertools
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
        # locs_left_by_block[b][val] contains a set with all the block cell nums of val in block b
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
            self.remove_possibility_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.x_cell_list[c.x]:
            self.remove_possibility_from_puzzle_by_cell_name(other_name, val)
        for other_name in self.block_cell_list[c.block]:
            self.remove_possibility_from_puzzle_by_cell_name(other_name, val)

    def remove_possibility_from_puzzle_by_loc(self, y, x, val):
        """
        Removes the val from the cell at position (y,x)'s possibilities.
        Also removes the val from the locs_left_by dicts
        :param y: The y location of the cell. Precondition: 0 <= y < 9
        :param x: The x location of the cell. Precondition: 0 <= x < 9
        :param val: The value to remove. Precondition: 1 <= val <= 9
        """
        cell_name = self.board[y][x]
        self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibility_from_puzzle_by_cell_name(self, cell_name, val):
        """
        Removes the val from the cell's possibilities.
        Also removes the val from the locs_left_by dicts
        :param cell_name: The name of the cell
        :param val: The value to remove. Precondition: 1 <= val <= 9
        """
        cell = self.cells_dict[cell_name]
        cell.remove_possibility(val)
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
        :param y: The row number. Precondition: 0 <= y < 9
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
        :param x: The col number. Precondition: 0 <= y < 9
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
        :param block_num: The block number. Precondition: 0 <= y < 9
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

    @staticmethod
    def find_unique_offsets_for_cell_nums(block_cell_nums):
        """
        :param block_cell_nums: The block cell numbers. Precondition: 0 <= n < 9 for n in block_cell_nums
        :param val: The val to find. Precondition: 1 <= val <= 9
        :return: (y_offsets, x_offsets) where:
        y_offsets is a set containing the row offsets. Will contain a subset of {0, 1, 2}
        x_offsets is a set containing the col offsets. Will contain a subset of {0, 1, 2}
        """
        y_offsets = set()
        x_offsets = set()
        for cell_num in block_cell_nums:
            y_offset, x_offset = SudokuHelper.cell_num_to_block_offsets(cell_num)
            y_offsets.add(y_offset)
            x_offsets.add(x_offset)
        return y_offsets, x_offsets

    def remove_possibility_not_in_block_with_y_offset(self, block_num, y_offset, val):
        """
        Removes the val from the possibilities not in the block with a y_offset
        For instance, if block_num = 3, y_offset = 2, val = 4
        then 4 would be removed from row 5 since row = y_block + y_offset = 3 + 2
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param y_offset: The y-offset in the block. Precondition: 0 <= y_offset < 3
        :param val: The val to find. Precondition: 1 <= val <= 9
        """
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        y = y_block + y_offset
        for cell_name in self.y_cell_list[y]:
            if self.cells_dict[cell_name].block != block_num:
                self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibility_not_in_block_with_x_offset(self, block_num, x_offset, val):
        """
        Removes the val from the possibilities not in the block with a x_offset
        For instance, if block_num = 3, x_offset = 2, val = 4
        then 4 would be removed from col 2 since row = y_block + y_offset = 0 + 2
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param x_offset: The x-offset in the block. Precondition: 0 <= x_offset < 3
        :param val: The val to find. Precondition: 1 <= val <= 9
        """
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        x = x_block + x_offset
        for cell_name in self.x_cell_list[x]:
            if self.cells_dict[cell_name].block != block_num:
                self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def block_rc_interaction(self, block_num):
        """
        Perform all block and row/column interactions involving the block
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        """
        for val in copy.deepcopy(self.remaining_in_blocks[block_num]):
            cell_nums = self.locs_left_by_block[block_num][val]
            y_offsets, x_offsets = SudokuPuzzle.find_unique_offsets_for_cell_nums(cell_nums)
            if len(y_offsets) == 1:
                y_offset = next(iter(y_offsets))
                self.remove_possibility_not_in_block_with_y_offset(block_num, y_offset, val)
            if len(x_offsets) == 1:
                x_offset = next(iter(x_offsets))
                self.remove_possibility_not_in_block_with_x_offset(block_num, x_offset, val)

    def all_block_rc_interactions(self):
        for block_num in all_locs:
            self.block_rc_interaction(block_num)

    def remove_possibilities_in_block_not_in_row(self, block_num, y, possibilities):
        """
        Removes possibilities from the cells of a block where row != y
        :param block_num: The block number of the block to remove possibilities from. Precondition: 0 <= block_num < 9
        :param y: The row number of cells to ignore. Precondition: 0 <= y < 9
        :param possibilities: The possibilities to remove. Precondition: 1 <= val <= 9 for val in possibilities
        """
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.y != y:
                for val in possibilities:
                    self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibilities_in_block_not_in_col(self, block_num, x, possibilities):
        """
        Removes possibilities from the cells of a block where col != x
        :param block_num: The block number of the block to remove possibilities from. Precondition: 0 <= block_num < 9
        :param x: The col number of cells to ignore. Precondition: 0 <= x < 9
        :param possibilities: The possibilities to remove. Precondition: 1 <= val <= 9 for val in possibilities
        """
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.x != x:
                for val in possibilities:
                    self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def block_block_interaction_horizontal(self, excluded_block_num):
        """
        Performs all block block interactions by row.
        i.e. eliminates possibilities from the excluded block based on the other two blocks in the row
        :param excluded_block_num: The block number to exclude. Precondition: 0 <= excluded_block_num < 9
        """
        excluded_block_possibilities = copy.deepcopy(self.remaining_in_blocks[excluded_block_num])
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(excluded_block_num)
        for y_offset in cell_locs:
            y = y_offset + y_block
            row_possibilities = self.remaining_in_y[y]
            possibilities = excluded_block_possibilities.intersection(row_possibilities)
            # Only keep the possibilities that are in the row and only found in the excluded block
            for cell_name in self.y_cell_list[y]:
                cell = self.cells_dict[cell_name]
                if cell.block != excluded_block_num:
                    possibilities.difference_update(cell.possibilities)
            # Remove the possibilities from the cells in the block which are not in the row
            self.remove_possibilities_in_block_not_in_row(excluded_block_num, y, possibilities)

    def block_block_interaction_vertical(self, excluded_block_num):
        """
        Performs all block block interactions by col.
        i.e. eliminates possibilities from the excluded block based on the other two blocks in the col
        :param excluded_block_num: The block number to exclude. Precondition: 0 <= excluded_block_num < 9
        """
        excluded_block_possibilities = copy.deepcopy(self.remaining_in_blocks[excluded_block_num])
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(excluded_block_num)
        for x_offset in cell_locs:
            x = x_offset + x_block
            col_possibilities = self.remaining_in_x[x]
            possibilities = excluded_block_possibilities.intersection(col_possibilities)
            # Only keep the possibilities that are in the col and only found in the excluded block
            for cell_name in self.x_cell_list[x]:
                cell = self.cells_dict[cell_name]
                if cell.block != excluded_block_num:
                    possibilities.difference_update(cell.possibilities)
            # Remove the possibilities from the cells in the block which are not in the row
            self.remove_possibilities_in_block_not_in_col(excluded_block_num, x, possibilities)

    def all_block_block_interactions(self):
        for block_num in all_locs:
            self.block_block_interaction_horizontal(block_num)
        for block_num in all_locs:
            self.block_block_interaction_vertical(block_num)

    @staticmethod
    def get_naked_pair_vals_in_possibilities_dict(possibilities_dict):
        """
        :param possibilities_dict: A dictionary with key = offsets and value = the possibilities
        :return: A list of (offset, vals) tuples corresponding to the offsets with matching possibilities
        i.e. get_naked_pairs_in_possibilities({0: [4, 7], 1: [2, 3], 3: [2, 3], 6: [4, 7], 8: [0, 7], 9: [2, 3]})
        returns: [((0, 6), [4, 7]), ((1, 3), [2, 3]), ((1, 9), [2, 3]), ((3, 9), [2, 3])]
        """
        l = len(possibilities_dict)
        if l < 2:
            return []
        keys = list(possibilities_dict.keys())
        naked_pairs_vals = []
        for m in range(0, l):
            vals = possibilities_dict[keys[m]]
            for n in range(m+1, l):
                if vals == possibilities_dict[keys[n]]:
                    naked_pairs_vals.append(((keys[m], keys[n]), vals))
        return naked_pairs_vals

    @staticmethod
    def get_naked_tuple_vals_in_possibilities_dict(possibilities_dict, n):
        """
        :param possibilities_dict: A dictionary with key = offsets and value = the possibilities
        :param n: The max number of unique vals in find within n items in possibilities_dict
        :return: A list of (offset, vals) tuples corresponding to the offsets with matching possibilities
        i.e. get_naked_tuples_in_possibilities_dict({0: [2, 5], 1: [1, 2, 5], 3: [3, 4, 5, 7, 8],
            7: [1, 5]}, 8: [4, 5, 6, 7]})
        returns: [((0, 1, 7), [1, 2, 5])]
        """
        l = len(possibilities_dict)
        if l < n:
            return []
        keys = list(possibilities_dict.keys())
        naked_tuples_vals = []
        for offset_tuple in itertools.combinations(keys, n):
            combined_possibilities = set()
            combination_works = True
            for i in range(0, n):
                combined_possibilities.update(possibilities_dict[offset_tuple[i]])
                if len(combined_possibilities) > n:
                    combination_works = False
                    break
            if combination_works:
                naked_tuples_vals.append((offset_tuple, combined_possibilities))
        return naked_tuples_vals

    def eliminate_possibilities_from_row(self, y, vals, x_to_exclude):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        :param vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in vals
        :param x_to_exclude: A tuple/list containing the x-offsets to ignore in the row.
        Precondition: 0 <= x < 9 for x in x_to_exclude
        Eliminates vals from the possibilities of all cells in the row except the ones with x-offsets in x_to_exclude.
        """
        for cell_name in self.y_cell_list[y]:
            cell = self.cells_dict[cell_name]
            if cell.x not in x_to_exclude:
                for val in vals:
                    self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def eliminate_possibilities_from_col(self, x, vals, y_to_exclude):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        :param vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in vals
        :param y_to_exclude: A tuple/list containing the y-offsets to ignore in the col
        Precondition: 0 <= y < 9 for y in y_to_exclude
        Eliminates vals from the possibilities of all cells in the col except the ones with y-offsets in y_to_exclude.
        """
        for cell_name in self.x_cell_list[x]:
            cell = self.cells_dict[cell_name]
            if cell.y not in y_to_exclude:
                for val in vals:
                    self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def eliminate_possibilities_from_block(self, block_num, vals, block_cell_nums_to_exclude):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in vals
        :param block_cell_nums_to_exclude: A tuple/list containing the block-cell--offsets to ignore in the block
        Precondition: 0 <= block_cell_num < 9 for block_cell_num in block_cell_nums_to_exclude
        Eliminates vals from the possibilities of all cells in the block except the ones with block-cell-offsets in
        block_cell_nums_to_exclude.
        """
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.block_cell_num not in block_cell_nums_to_exclude:
                for val in vals:
                    self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def naked_pair_y(self, y):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        Finds naked pairs in the row and eliminates possibilities accordingly
        """
        row_possibilities = self.enumerate_row_possibilities(y)
        row_dict = {x: row_possibilities[x] for x in all_locs if len(row_possibilities[x]) == 2}
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(row_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            self.eliminate_possibilities_from_row(y, vals, offset_pair)

    def naked_pair_x(self, x):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        Finds naked pairs in the col and eliminates possibilities accordingly
        """
        col_possibilities = self.enumerate_col_possibilities(x)
        col_dict = {y: col_possibilities[y] for y in all_locs if len(col_possibilities[y]) == 2}
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(col_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            self.eliminate_possibilities_from_col(x, vals, offset_pair)

    def naked_pair_block(self, block_num):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        Finds naked pairs in the block and eliminates possibilities accordingly
        """
        block_possibilities = self.enumerate_block_possibilities(block_num)
        block_dict = {c: block_possibilities[c] for c in all_locs if len(block_possibilities[c]) == 2}
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(block_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            self.eliminate_possibilities_from_block(block_num, vals, offset_pair)

    def naked_tuple_y(self, y, n):
        row_possibilities = self.enumerate_row_possibilities(y)
        row_dict = {x: row_possibilities[x] for x in all_locs if len(row_possibilities[x]) <= n}
        naked_offset_tuples = SudokuPuzzle.get_naked_tuple_vals_in_possibilities_dict(row_dict)
        for (offset_tuple, vals) in naked_offset_tuples:
            self.eliminate_possibilities_from_row(y, vals, offset_tuple)

    def enumerate_row_possibilities(self, y):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        :return: A list with all the possibilities in the row, listed in order
        """
        row_possibilities = []
        for x in all_locs:
            row_possibilities.append(self.cells_dict[self.board[y][x]].possibilities)
        return row_possibilities

    def enumerate_col_possibilities(self, x):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        :return: A list with all the possibilities in the col, listed in order
        """
        col_possibilities = []
        for y in all_locs:
            col_possibilities.append(self.cells_dict[self.board[y][x]].possibilities)
        return col_possibilities

    def enumerate_block_possibilities(self, block_num):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :return: A list with all the possibilities in the block, listed in order
        """
        block_possibilities = []
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        for y_offset in cell_locs:
            for x_offset in cell_locs:
                p = self.cells_dict[self.board[y_block + y_offset][x_block + x_offset]].possibilities
                block_possibilities.append(p)
        return block_possibilities

    def print_board(self):
        """
        Pretty prints the filled in values for the board
        """
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
        """
        Pretty prints the board possibilities
        """
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
        """
        :param board: The board to rotate
        :param n: The number of times to rotate
        :return: The board rotated clockwise n times
        """
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
        """
        :param board: The board to rotate
        :param n: The number of times to rotate
        :return: The board rotated counterclockwise n times
        """
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
        """
        :param board: The board to reflect
        :return: The board reflected over the xy-axis. i.e. board[y][x] -> reflected_board[x][y]
        """
        rotated_board = [[None for _ in all_locs] for _ in all_locs]
        for y in all_locs:
            for x in all_locs:
                rotated_board[y][x] = board[x][y]
        return rotated_board
