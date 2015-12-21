from collections import defaultdict
import copy
import itertools
from SudokuError import BadGuessError
from SudokuError import BadPuzzleError
from SudokuCell import SudokuCell
from SudokuGuess import SudokuGuess
from SudokuHelper import all_locs
from SudokuHelper import cell_locs
from SudokuHelper import all_possibilities
from SudokuStep import SudokuStep
import SudokuHelper

__author__ = 'william'


class SudokuPuzzle:

    def __init__(self, board=None):
        # Static variables
        # A 2D-matrix containing cell names
        self.board = [[None for x in all_locs] for y in all_locs]
        # y_cell_list[n] contains a set with the names for each cell in row n
        self.y_cell_list = [set() for _ in all_locs]
        # x_cell_list[n] contains a set with the names for each cell in col n
        self.x_cell_list = [set() for _ in all_locs]
        # block_cell_list[n] contains a set with the names for each cell in block n
        self.block_cell_list = [set() for _ in all_locs]

        # Instance variables
        # A dictionary from cell name to the SudokuCell object
        self.cells_dict = {}
        # remaining_in_y[n] contains the remaining values in row n
        self.remaining_in_y = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # remaining_in_x[n] contains the remaining values in col n
        self.remaining_in_x = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # remaining_in_blocks[n] contains the remaining values in block n
        self.remaining_in_blocks = [copy.deepcopy(all_possibilities) for _ in all_locs]
        # locs_left_by_y[y][val] contains a set with all the possible x-offsets of val in row y
        self.locs_left_by_y = [defaultdict(set) for y in all_locs]
        # locs_left_by_x[x][val] contains a set with all the possible y-offsets of val in col x
        self.locs_left_by_x = [defaultdict(set) for x in all_locs]
        # locs_left_by_block[b][val] contains a set with all the possible block cell nums of val in block b
        self.locs_left_by_block = [defaultdict(set) for block_num in all_locs]
        # guess contains a None or a SudokuGuess object
        self.guess = None
        # The number of cells with filled in values
        self.num_filled = 0

        if board is not None:
            self.initialize_new_puzzle(board)

    def determine_next_guess(self):
        """
        Finds a reasonable next guess
        :return: (cell_name, candidate) corresponding to a reasonable next guess
        If a reasonable guess cannot be found, return None
        """
        for n in range(2, 9):
            for (cell_name, cell) in self.cells_dict.items():
                if len(cell.possibilities) == n:
                    candidate = next(iter(cell.possibilities))
                    return cell_name, candidate
        return None, None

    def make_guess(self, cell_name, candidate):
        """
        :param candidate: The candidate which is thought to be in the location of cell_name
        :param cell_name: The cell name which is thought to contain the candidate
        Sets self.guess according to the candidate and cell_name of the next guess
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) of the guess
        """
        self.guess = SudokuGuess(candidate, cell_name, self.cells_dict, self.guess, self.num_filled)
        updated_cells = self.set_val_in_puzzle_by_cell_name(cell_name, candidate)
        return SudokuStep((cell_name, candidate), updated_cells, "Guessing " + str(candidate) + " into " + cell_name)

    def revert_guess(self):
        """
        Reverts the SudokuPuzzle to the previous state before the current guess
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = {(cell name, removed possibility)} corresponding to the reverted guess
        """
        if self.guess:
            self.cells_dict = self.guess.previous_cells_dict
            cell_name = self.guess.guess_cell_name
            candidate = self.guess.guess_candidate
            self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate)
            self.num_filled = self.guess.num_filled
            self.guess = self.guess.previous_guess
            self.recalculate_fields()
            return SudokuStep(None, {(cell_name, candidate)},
                              "Reverting Guess of " + str(candidate) + " into " + cell_name)

    def validate_updated_cells_ignoring_newly_set_val(self, updated_cells, cell_name):
        """
        :param updated_cells: A list of (other_name, val) tuples set by the previous method
        Raises a BadGuessError if removing the possibilities causes the Sudoku Puzzle to break any rules.
        However, it ignores any errors coming from the cell which was just set (cell_name)
        i.e. A candidate can no longer be placed in every row/col/block or a cell has an empty set for possibilities
        """
        cell = self.cells_dict[cell_name]
        for (other_name, val) in updated_cells:
            other_cell = self.cells_dict[other_name]
            if other_cell.possibilities is None or len(other_cell.possibilities) == 0:
                raise BadGuessError(other_name, val, "No more possibilities for cell " + other_name)
            if cell.y != other_cell.y and (self.locs_left_by_y[other_cell.y][val] is None or len(
                    self.locs_left_by_y[other_cell.y][val]) == 0):
                raise BadGuessError(other_name, val, "Can't place " + str(val) + " in row " + str(other_cell.y))
            if cell.x != other_cell.x and (self.locs_left_by_x[other_cell.x][val] is None or len(
                    self.locs_left_by_x[other_cell.x][val]) == 0):
                raise BadGuessError(other_name, val, "Can't place " + str(val) + " in col " + str(other_cell.x))
            if cell.block != other_cell.block and (self.locs_left_by_block[other_cell.block][val] is None or len(
                    self.locs_left_by_block[other_cell.block][val]) == 0):
                raise BadGuessError(other_name, val, "Can't place " + str(val) + " in block " + str(other_cell.block))

    def validate_updated_cells(self, updated_cells):
        """
        :param updated_cells: A list of (cell_name, val) tuples set by this method
        Raises a BadGuessError if removing the possibilities causes the Sudoku Puzzle to break any rules.
        i.e. A candidate can no longer be placed in every row/col/block or a cell has an empty set for possibilities
        """
        for (cell_name, val) in updated_cells:
            cell = self.cells_dict[cell_name]
            if cell.possibilities is None or len(cell.possibilities) == 0:
                raise BadGuessError(cell_name, val, "No more possibilities for cell " + cell_name)
            if self.locs_left_by_y[cell.y][val] is None or len(self.locs_left_by_y[cell.y][val]) == 0:
                raise BadGuessError(cell_name, val, "Can't place " + str(val) + " in row " + str(cell.y))
            if self.locs_left_by_x[cell.x][val] is None or len(self.locs_left_by_x[cell.x][val]) == 0:
                raise BadGuessError(cell_name, val, "Can't place " + str(val) + " in col " + str(cell.x))
            if self.locs_left_by_block[cell.block][val] is None or len(self.locs_left_by_block[cell.block][val]) == 0:
                raise BadGuessError(cell_name, val, "Can't place " + str(val) + " in block " + str(cell.block))

    def initialize_new_puzzle(self, board):
        """
        Used when initializing a new puzzle
        :param board: A 2D-matrix containing known values
        """
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

        illegal_cells = self.validate_board()
        if illegal_cells:
            raise BadPuzzleError(illegal_cells)

        # Calculate remaining_in and locs_left_by fields
        self.recalculate_fields()

    def recalculate_fields(self):
        """
        Recalculate the remaining_in and locs_left_by fields based on the cells_dict
        """
        self.remaining_in_y = [copy.deepcopy(all_possibilities) for _ in all_locs]
        self.remaining_in_x = [copy.deepcopy(all_possibilities) for _ in all_locs]
        self.remaining_in_blocks = [copy.deepcopy(all_possibilities) for _ in all_locs]

        for cell_name in self.cells_dict.keys():
            cell = self.cells_dict[cell_name]
            if cell.val:
                self.remaining_in_y[cell.y].discard(cell.val)
                self.remaining_in_x[cell.x].discard(cell.val)
                self.remaining_in_blocks[cell.block].discard(cell.val)
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
        :return: A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        cell_name = self.board[y][x]
        return self.set_val_in_puzzle_by_cell_name(cell_name, val)

    def set_val_in_puzzle_by_cell_name(self, cell_name, val):
        """
        Sets the cell with the provided cell_name to the val.
        Removes possibilities from remaining_in and locs_left_by fields
        :param cell_name: The cell_name of the cell.
        :param val: The value to set. Precondition: 1 <= val <= 9
        :return: A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        c = self.cells_dict[cell_name]
        self.remaining_in_y[c.y].discard(val)
        self.remaining_in_x[c.x].discard(val)
        self.remaining_in_blocks[c.block].discard(val)
        self.locs_left_by_y[c.y][val].discard(c.x)
        self.locs_left_by_x[c.x][val].discard(c.y)
        self.locs_left_by_block[c.block][val].discard(c.block_cell_num)
        c.set_val(val)
        self.num_filled += 1

        # Remove possibilities from row, col, block
        for other_name in self.y_cell_list[c.y]:
            if self.remove_possibility_from_puzzle_by_cell_name(other_name, val):
                updated_cells.add((other_name, val))
        for other_name in self.x_cell_list[c.x]:
            if self.remove_possibility_from_puzzle_by_cell_name(other_name, val):
                updated_cells.add((other_name, val))
        for other_name in self.block_cell_list[c.block]:
            if self.remove_possibility_from_puzzle_by_cell_name(other_name, val):
                updated_cells.add((other_name, val))
        return updated_cells

    # region Remove Possibilities
    # region Remove Single Possibility from puzzle
    def remove_possibility_from_puzzle_by_loc(self, y, x, val):
        """
        Removes the val from the cell at position (y,x)'s possibilities.
        Also removes the val from the locs_left_by dicts
        :param y: The y location of the cell. Precondition: 0 <= y < 9
        :param x: The x location of the cell. Precondition: 0 <= x < 9
        :param val: The value to remove. Precondition: 1 <= val <= 9
        :return True if the possibility was removed. False otherwise
        """
        cell_name = self.board[y][x]
        return self.remove_possibility_from_puzzle_by_cell_name(cell_name, val)

    def remove_possibility_from_puzzle_by_cell_name(self, cell_name, val):
        """
        Removes the val from the cell's possibilities.
        Also removes the val from the locs_left_by dicts
        :param cell_name: The name of the cell
        :param val: The value to remove. Precondition: 1 <= val <= 9
        :return True if the possibility was actually removed. False otherwise
        """
        cell = self.cells_dict[cell_name]
        val_removed = False
        if cell.val is None:
            val_removed = cell.remove_possibility(val)
            self.locs_left_by_y[cell.y][val].discard(cell.x)
            self.locs_left_by_x[cell.x][val].discard(cell.y)
            self.locs_left_by_block[cell.block][val].discard(cell.block_cell_num)
        return val_removed
    # endregion

    # region Eliminate Possibilities from Row/Col/Block (except excluded)
    def eliminate_possibilities_from_row(self, y, vals, x_to_exclude):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        :param vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in vals
        :param x_to_exclude: A tuple/list containing the x-offsets to ignore in the row.
        Precondition: 0 <= x < 9 for x in x_to_exclude
        Eliminates vals from the possibilities of all cells in the row except the ones with x-offsets in x_to_exclude.
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.y_cell_list[y]:
            cell = self.cells_dict[cell_name]
            if cell.x not in x_to_exclude:
                for val in vals:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
        return updated_cells

    def eliminate_possibilities_from_col(self, x, vals, y_to_exclude):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        :param vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in vals
        :param y_to_exclude: A tuple/list containing the y-offsets to ignore in the col
        Precondition: 0 <= y < 9 for y in y_to_exclude
        Eliminates vals from the possibilities of all cells in the col except the ones with y-offsets in y_to_exclude.
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.x_cell_list[x]:
            cell = self.cells_dict[cell_name]
            if cell.y not in y_to_exclude:
                for val in vals:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
        return updated_cells
    # endregion

    # region Eliminate Other Possibilities with Row/Col/Block offsets (except excluded)
    def eliminate_other_possibilities_from_cells_in_row(self, y, excluded_vals, offsets):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        :param excluded_vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in excluded_vals
        :param offsets: An enumerable containing the row offsets from which to eliminate all other candidates other
        than the ones in excluded_vals
        Eliminates candidates not in excluded_vals from the possibilities of cells in the row with offset in offsets
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.y_cell_list[y]:
            cell = self.cells_dict[cell_name]
            if cell.x in offsets:
                possibilities_to_remove = cell.possibilities.difference(excluded_vals)
                for candidate in possibilities_to_remove:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate):
                        updated_cells.add((cell_name, candidate))
        return updated_cells

    def eliminate_other_possibilities_from_cells_in_col(self, x, excluded_vals, offsets):
        """
        :param x: The col number. Precondition: 0 <= y < 9
        :param excluded_vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in excluded_vals
        :param offsets: An enumerable containing the col offsets from which to eliminate all other candidates other
        than the ones in excluded_vals
        Eliminates candidates not in excluded_vals from the possibilities of cells in the col with offset in offsets
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.x_cell_list[x]:
            cell = self.cells_dict[cell_name]
            if cell.y in offsets:
                possibilities_to_remove = cell.possibilities.difference(excluded_vals)
                for candidate in possibilities_to_remove:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate):
                        updated_cells.add((cell_name, candidate))
        return updated_cells

    def eliminate_other_possibilities_from_cells_in_block(self, block_num, excluded_vals, offsets):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param excluded_vals: A set containing the values to eliminate. Precondition: 1 <= val <= 9 for val in excluded_vals
        :param offsets: An enumerable containing the block-cell-offsets from which to eliminate all other
        candidates other than the ones in excluded_vals
        Eliminates candidates not in excluded_vals from the possibilities of cells in the block with block cell nums in
        block-cell-nums
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.block_cell_num in offsets:
                possibilities_to_remove = cell.possibilities.difference(excluded_vals)
                for candidate in possibilities_to_remove:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate):
                        updated_cells.add((cell_name, candidate))
        return updated_cells

    def eliminate_other_possibilities_from_other_cells_in_block(self, block_num, excluded_vals, other_block_cell_nums):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param excluded_vals: A set containing the values to eliminate.
        Precondition: 1 <= val <= 9 for val in excluded_vals
        :param other_block_cell_nums: A tuple/list containing the block-cell-offsets to ignore in the block
        Precondition: 0 <= block_cell_num < 9 for block_cell_num in other_block_cell_nums
        Eliminates all possibilities from the the cells in other_block_cell_nums except for the ones in excluded_vals.
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.block_cell_num not in other_block_cell_nums:
                for val in excluded_vals:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
        return updated_cells

    # endregion

    # region Eliminate possibility in Row/Col not in Block
    def remove_possibility_not_in_block_with_y_offset(self, block_num, y_offset, val):
        """
        Removes the val from the possibilities not in the block with a y_offset
        For instance, if block_num = 3, y_offset = 2, val = 4
        then 4 would be removed from row 5 since row = y_block + y_offset = 3 + 2
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param y_offset: The y-offset in the block. Precondition: 0 <= y_offset < 3
        :param val: The val to find. Precondition: 1 <= val <= 9
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        y = y_block + y_offset
        for cell_name in self.y_cell_list[y]:
            if self.cells_dict[cell_name].block != block_num:
                if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                    updated_cells.add((cell_name, val))
        return updated_cells

    def remove_possibility_not_in_block_with_x_offset(self, block_num, x_offset, val):
        """
        Removes the val from the possibilities not in the block with a x_offset
        For instance, if block_num = 3, x_offset = 2, val = 4
        then 4 would be removed from col 2 since row = y_block + y_offset = 0 + 2
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param x_offset: The x-offset in the block. Precondition: 0 <= x_offset < 3
        :param val: The val to find. Precondition: 1 <= val <= 9
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        y_block, x_block = SudokuHelper.block_num_to_block_offsets(block_num)
        x = x_block + x_offset
        for cell_name in self.x_cell_list[x]:
            if self.cells_dict[cell_name].block != block_num:
                if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                    updated_cells.add((cell_name, val))
        return updated_cells
    # endregion

    # region Eliminate possibilities in Block not in Row/Col
    def remove_possibilities_in_block_not_in_row(self, block_num, y, possibilities):
        """
        Removes possibilities from the cells of a block where row != y
        :param block_num: The block number of the block to remove possibilities from. Precondition: 0 <= block_num < 9
        :param y: The row number of cells to ignore. Precondition: 0 <= y < 9
        :param possibilities: The possibilities to remove. Precondition: 1 <= val <= 9 for val in possibilities
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.y != y:
                for val in possibilities:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
        return updated_cells

    def remove_possibilities_in_block_not_in_col(self, block_num, x, possibilities):
        """
        Removes possibilities from the cells of a block where col != x
        :param block_num: The block number of the block to remove possibilities from. Precondition: 0 <= block_num < 9
        :param x: The col number of cells to ignore. Precondition: 0 <= x < 9
        :param possibilities: The possibilities to remove. Precondition: 1 <= val <= 9 for val in possibilities
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        for cell_name in self.block_cell_list[block_num]:
            cell = self.cells_dict[cell_name]
            if cell.x != x:
                for val in possibilities:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
        return updated_cells
    # endregion
    # endregion

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

    # region Sole Candidates
    def fill_sole_candidate(self):
        """
        Fills in a sole candidate
        i.e. when a specific cell can only contain a single number
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) tuple set by this method
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for cell_name in self.cells_dict.keys():
            cell = self.cells_dict[cell_name]
            if cell.val is None and len(cell.possibilities) == 1:
                val = next(iter(cell.possibilities))
                updated_cells = (self.set_val_in_puzzle_by_cell_name(cell_name, val))
                description = "Sole Candidate: " + str(val) + " is the last candidate for " + str(cell_name)
                return SudokuStep((cell_name, val), updated_cells, description)
        return None
    # endregion

    # region Unique Candidates
    def fill_unique_candidate_y(self, y):
        """
        Fills in a unique candidates by row
        i.e. when a number can only go in one spot in row y
        :param y: The row number. Precondition: 0 <= y < 9
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) tuple set by this method
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        y_locs_left = self.locs_left_by_y[y]
        y_possibilities = self.remaining_in_y[y]
        for val in copy.deepcopy(y_possibilities):
            if len(y_locs_left[val]) == 1:
                cell_name = self.board[y][next(iter(y_locs_left[val]))]
                updated_cells = self.set_val_in_puzzle_by_cell_name(cell_name, val)
                description = "Unique Candidate: " + cell_name + " is the only remaining location for " + str(val) +\
                              " in row " + str(y)
                return SudokuStep((cell_name, val), updated_cells, description)
        return None

    def fill_unique_candidate_x(self, x):
        """
        Fills in unique candidates by col
        i.e. when a number can only go in one spot in col x
        :param x: The col number. Precondition: 0 <= y < 9
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) tuple set by this method
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        x_locs_left = self.locs_left_by_x[x]
        x_possibilities = self.remaining_in_x[x]
        for val in copy.deepcopy(x_possibilities):
            if len(x_locs_left[val]) == 1:
                cell_name = self.board[next(iter(x_locs_left[val]))][x]
                updated_cells = self.set_val_in_puzzle_by_cell_name(cell_name, val)
                description = "Unique Candidate: " + cell_name + " was the only remaining location for " + str(val) +\
                              " in col " + str(x)
                return SudokuStep((cell_name, val), updated_cells, description)
        return None

    def fill_unique_candidate_block(self, block_num):
        """
        Fills in unique candidates by block
        i.e. when a number can only go in one spot in block block_number
        :param block_num: The block number. Precondition: 0 <= y < 9
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) tuple set by this method
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        block_locs_left = self.locs_left_by_block[block_num]
        block_possibilities = self.remaining_in_blocks[block_num]
        for val in copy.deepcopy(block_possibilities):
            if len(block_locs_left[val]) == 1:
                (y, x) = SudokuHelper.block_num_and_cell_num_to_offsets(
                    block_num, next(iter(block_locs_left[val])))
                cell_name = self.board[y][x]
                updated_cells = self.set_val_in_puzzle_by_cell_name(cell_name, val)
                description = "Unique Candidate: " + cell_name + " was the only remaining location for " + str(val) +\
                              " in block " + str(block_num)
                return SudokuStep((cell_name, val), updated_cells, description)
        return None

    def fill_unique_candidate(self):
        """
        Fills in a unique candidate
        i.e. when a number can only go in one spot in a row/col/block
        :return A SudokuStep corresponding to the guess where:
                * filled_cell = (cell_name, candidate) tuple set by this method
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for y in all_locs:
            ss = self.fill_unique_candidate_y(y)
            if ss:
                return ss
        for x in all_locs:
            ss = self.fill_unique_candidate_x(x)
            if ss:
                return ss
        for block_num in all_locs:
            ss = self.fill_unique_candidate_block(block_num)
            if ss:
                return ss
        return None
    # endregion

    @staticmethod
    def find_unique_offsets_for_cell_nums(block_cell_nums):
        """
        :param block_cell_nums: The block cell numbers. Precondition: 0 <= n < 9 for n in block_cell_nums
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

    # region Block-Row/Column Interactions
    def block_rc_interaction(self, block_num):
        """
        Perform all block and row/column interactions involving the block
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for val in copy.deepcopy(self.remaining_in_blocks[block_num]):
            (y_block, x_block) = SudokuHelper.block_num_to_block_offsets(block_num)
            cell_nums = self.locs_left_by_block[block_num][val]
            y_offsets, x_offsets = SudokuPuzzle.find_unique_offsets_for_cell_nums(cell_nums)
            if len(y_offsets) == 1:
                y_offset = next(iter(y_offsets))
                updated_cells = self.remove_possibility_not_in_block_with_y_offset(block_num, y_offset, val)
                if updated_cells:
                    description = "Block-Row Interaction: Eliminated " + str(val) + " in row " + \
                                  str((y_block + y_offset)) + " not in block " + str(block_num)
                    return SudokuStep(None, updated_cells, description)
            if len(x_offsets) == 1:
                x_offset = next(iter(x_offsets))
                updated_cells = self.remove_possibility_not_in_block_with_x_offset(block_num, x_offset, val)
                if updated_cells:
                    description = "Block-Col Interaction: Eliminated " + str(val) + " in col " \
                                  + str((x_block + x_offset)) + " not in block " + str(block_num)
                    return SudokuStep(None, updated_cells, description)
        return None

    def perform_block_rc_interaction(self):
        """
        Perform all block and row/column interactions
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for block_num in all_locs:
            ss = self.block_rc_interaction(block_num)
            if ss:
                return ss
        return None
    # endregion

    # region Block-Block Interactions
    def block_block_interaction_horizontal(self, excluded_block_num):
        """
        Performs all block block interactions by row.
        i.e. eliminates possibilities from the excluded block based on the other two blocks in the row
        :param excluded_block_num: The block number to exclude. Precondition: 0 <= excluded_block_num < 9
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
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
            if possibilities:
                # Remove the possibilities from the cells in the block which are not in the row
                updated_cells = self.remove_possibilities_in_block_not_in_row(excluded_block_num, y, possibilities)
                if updated_cells:
                    description = "Block-Block Interaction Horizontal: Removed " + str(possibilities) + " in row " \
                                  + str(y) + " which were not in block " + str(excluded_block_num)
                    return SudokuStep(None, updated_cells, description)
        return None

    def block_block_interaction_vertical(self, excluded_block_num):
        """
        Performs all block block interactions by col.
        i.e. eliminates possibilities from the excluded block based on the other two blocks in the col
        :param excluded_block_num: The block number to exclude. Precondition: 0 <= excluded_block_num < 9
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
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
            if possibilities:
                # Remove the possibilities from the cells in the block which are not in the row
                updated_cells = self.remove_possibilities_in_block_not_in_col(excluded_block_num, x, possibilities)
                if updated_cells:
                    description = "Block-Block Interaction Vertical: Removed " + str(possibilities) + " in col " \
                                  + str(x) + " which were not in block " + str(excluded_block_num)
                    return SudokuStep(None, updated_cells, description)
        return None

    def perform_block_block_interaction(self):
        """
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for block_num in all_locs:
            ss = self.block_block_interaction_horizontal(block_num)
            if ss:
                return ss
        for block_num in all_locs:
            ss = self.block_block_interaction_vertical(block_num)
            if ss:
                return ss
        return None
    # endregion

    @staticmethod
    def get_naked_pair_vals_in_possibilities_dict(possibilities_dict):
        """
        :param possibilities_dict: A dictionary with key = offsets and value = the possibilities
        :return: A list of (offset, vals) tuples corresponding to the offsets with matching possibilities
        i.e. get_naked_pairs_in_possibilities({0: [4, 7], 1: [2, 3], 3: [2, 3],
        6: [4, 7], 7: [], 8: [0, 7], 9: [2, 3]})
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

    # region Naked Tuples
    def naked_pair_y(self, y):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        Finds naked pairs in the row and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        row_possibilities = self.enumerate_row_possibilities(y)
        row_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(row_possibilities, lambda l: l == 2)
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(row_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            updated_cells = self.eliminate_possibilities_from_row(y, vals, offset_pair)
            if updated_cells:
                description = "Naked Pair Row : In row " + str(y) + ", " + str(vals) \
                              + " are the only candidates for cells with x-offsets of " + str(offset_pair) \
                              + ".\nEliminating those candidates from all other cells in the row."
                return SudokuStep(None, updated_cells, description)
        return None

    def naked_pair_x(self, x):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        Finds naked pairs in the col and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        col_possibilities = self.enumerate_col_possibilities(x)
        col_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(col_possibilities, lambda l: l == 2)
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(col_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            updated_cells = self.eliminate_possibilities_from_col(x, vals, offset_pair)
            if updated_cells:
                description = "Naked Pair Col : In col " + str(x) + ", " + str(vals) \
                              + " are the only candidates for cells with y-offsets of " + str(offset_pair) \
                              + ".\nEliminating those candidates from all other cells in the col."
                return SudokuStep(None, updated_cells, description)
        return None

    def naked_pair_block(self, block_num):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        Finds naked pairs in the block and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        block_possibilities = self.enumerate_block_possibilities(block_num)
        block_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(block_possibilities, lambda l: l == 2)
        naked_offset_pairs = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(block_dict)
        for (offset_pair, vals) in naked_offset_pairs:
            updated_cells = self.eliminate_other_possibilities_from_other_cells_in_block(
                block_num, vals, offset_pair)
            if updated_cells:
                description = "Naked Pair Block : In block " + str(block_num) + ", " + str(vals) \
                              + " are the only candidates for cells with block-cell-offsets of " + str(offset_pair) \
                              + ".\nEliminating those candidates from all other cells in the block."
                return SudokuStep(None, updated_cells, description)
        return None

    def perform_naked_pair(self):
        """
        Finds naked tuples and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for y in all_locs:
            ss = self.naked_pair_y(y)
            if ss:
                return ss
        for x in all_locs:
            ss = self.naked_pair_x(x)
            if ss:
                return ss
        for block_num in all_locs:
            ss = self.naked_pair_block(block_num)
            if ss:
                return ss
        return None

    # NOTE: naked_tuple_[...] with n = 2 should behave pretty much exactly like naked_pair_[...]

    def naked_tuple_y(self, y, n):
        """
        :param y: The row number. Precondition: 0 <= y < 9
        :param n: The tuple size. Usually n <= 4
        Finds naked tuples in the row and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        row_possibilities = self.enumerate_row_possibilities(y)
        row_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(row_possibilities, lambda l: 0 < l <= n)
        naked_offset_tuples = SudokuPuzzle.get_naked_tuple_vals_in_possibilities_dict(row_dict, n)
        for (offset_tuple, vals) in naked_offset_tuples:
            updated_cells = self.eliminate_possibilities_from_row(y, vals, offset_tuple)
            if updated_cells:
                description = "Naked Tuple Row " + str(n) + ": In row " + str(y) + ", " + str(vals) \
                              + " are the only candidates for cells with x-offsets of " + str(offset_tuple) \
                              + ".\nEliminating those candidates from all other cells in the row."
                return SudokuStep(None, updated_cells, description)
        return None

    def naked_tuple_x(self, x, n):
        """
        :param x: The col number. Precondition: 0 <= x < 9
        :param n: The tuple size. Usually n <= 4
        Finds naked tuples in the col and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        col_possibilities = self.enumerate_col_possibilities(x)
        col_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(col_possibilities, lambda l: 0 < l <= n)
        naked_offset_tuples = SudokuPuzzle.get_naked_tuple_vals_in_possibilities_dict(col_dict, n)
        for (offset_tuple, vals) in naked_offset_tuples:
            updated_cells = self.eliminate_possibilities_from_col(x, vals, offset_tuple)
            if updated_cells:
                description = "Naked Tuple Col " + str(n) + ": In col " + str(x) + ", " + str(vals) \
                              + " are the only candidates for cells with y-offsets of " + str(offset_tuple) \
                              + ".\nEliminating those candidates from all other cells in the col."
                return SudokuStep(None, updated_cells, description)
        return None

    def naked_tuple_block(self, block_num, n):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param n: The tuple size. Usually n <= 4
        Finds naked tuples in the block and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        block_possibilities = self.enumerate_block_possibilities(block_num)
        block_dict = SudokuPuzzle.possibilities_to_dict_with_len_constraint(block_possibilities, lambda l: 0 < l <= n)
        naked_offset_tuples = SudokuPuzzle.get_naked_tuple_vals_in_possibilities_dict(block_dict, n)
        for (offset_tuple, vals) in naked_offset_tuples:
            updated_cells = self.eliminate_other_possibilities_from_other_cells_in_block(
                block_num, vals, offset_tuple)
            if updated_cells:
                description = "Naked Tuple Block " + str(n) + ": In block " + str(block_num) + ", " + str(vals) \
                              + " are the only candidates for cells with block-cell-offsets of " + str(offset_tuple) \
                              + ".\nEliminating those candidates from all other cells in the block."
                return SudokuStep(None, updated_cells, description)
        return None
    # endregion

    def perform_naked_tuple(self, n):
        """
        :param n: The tuple size. Usually n <= 4
        Finds naked tuples and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for y in all_locs:
            ss = self.naked_tuple_y(y, n)
            if ss:
                return ss
        for x in all_locs:
            ss = self.naked_tuple_x(x, n)
            if ss:
                return ss
        for block_num in all_locs:
            ss = self.naked_tuple_block(block_num, n)
            if ss:
                return ss
        return None

    @staticmethod
    def possibilities_to_dict_with_len_constraint(possibilities, len_lambda):
        """
        :param possibilities: The possibilities to create the dict from.
        Precondition: 1 <= val <= 9 for val in possibilities
        :param len_lambda: The lambda function to execute of the length of each possibility.
        Should be a function that takes in a length and returns true/false
        :return: A dictionary from a cell offset within a row/col/block to the possibilities in that cell given the
        possibilities satisfy the supplied lambda
        """
        return {offset: possibilities[offset] for offset in all_locs if len_lambda(len(possibilities[offset]))}

    # region Hidden Subset
    def hidden_subset_row(self, y, n):
        """
        :param: y: The row number. Precondition: 0 <= y < 9
        :param n: The number of candidates to find within the row
        Finds hidden subsets in the row and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        possibilities = self.remaining_in_y[y]
        locs_left = self.locs_left_by_y[y]
        for possibilities_tuple in itertools.combinations(possibilities, n):
            locations = set()
            hidden_subset_found = True
            for candidate in possibilities_tuple:
                locations.update(locs_left[candidate])
                if len(locations) > n:
                    hidden_subset_found = False
                    break
            if hidden_subset_found:
                excluded_vals = set(possibilities_tuple)
                updated_cells = self.eliminate_other_possibilities_from_cells_in_row(
                    y, excluded_vals, locations)
                if updated_cells:
                    description = "Hidden Subset Row " + str(n) + ": In row " + str(y) + ", " + str(excluded_vals) \
                              + " can only be placed in cells with x-offsets of " + str(locations) \
                              + ".\nEliminating all other candidates for those cells."
                    return SudokuStep(None, updated_cells, description)
        return None

    def hidden_subset_col(self, x, n):
        """
        :param x: The col number. Precondition: 0 <= y < 9
        :param n: The number of candidates to find within the col
        Finds hidden subsets in the row and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        possibilities = self.remaining_in_x[x]
        locs_left = self.locs_left_by_x[x]
        for possibilities_tuple in itertools.combinations(possibilities, n):
            locations = set()
            hidden_subset_found = True
            for candidate in possibilities_tuple:
                locations.update(locs_left[candidate])
                if len(locations) > n:
                    hidden_subset_found = False
                    break
            if hidden_subset_found:
                excluded_vals = set(possibilities_tuple)
                updated_cells = self.eliminate_other_possibilities_from_cells_in_col(
                    x, excluded_vals, locations)
                if updated_cells:
                    description = "Hidden Subset Col " + str(n) + ": In col " + str(x) + ", " + str(excluded_vals) \
                              + " can only be placed in cells with y-offsets of " + str(locations) \
                              + ".\nEliminating all other candidates for those cells."
                    return SudokuStep(None, updated_cells, description)
        return None

    def hidden_subset_block(self, block_num, n):
        """
        :param block_num: The block number. Precondition: 0 <= block_num < 9
        :param n: The number of candidates to find within the block
        Finds hidden subsets in the block and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        possibilities = self.remaining_in_blocks[block_num]
        locs_left = self.locs_left_by_block[block_num]
        for possibilities_tuple in itertools.combinations(possibilities, n):
            locations = set()
            hidden_subset_found = True
            for candidate in possibilities_tuple:
                locations.update(locs_left[candidate])
                if len(locations) > n:
                    hidden_subset_found = False
                    break
            if hidden_subset_found:
                excluded_vals = set(possibilities_tuple)
                updated_cells = self.eliminate_other_possibilities_from_cells_in_block(
                        block_num, set(possibilities_tuple), locations)
                if updated_cells:
                    description = "Hidden Subset Block " + str(n) + ": In block " + str(block_num) + ", " \
                                  + str(excluded_vals) + " can only be placed in cells with block-cell-offsets of " \
                                  + str(locations) + ".\nEliminating all other candidates for those cells."
                    return SudokuStep(None, updated_cells, description)
        return None

    def perform_hidden_subset(self, n):
        """
        :param n: The number of candidates to find
        Finds hidden subsets and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for y in all_locs:
            ss = self.hidden_subset_row(y, n)
            if ss:
                return ss
        for x in all_locs:
            ss = self.hidden_subset_row(x, n)
            if ss:
                return ss
        for block_num in all_locs:
            ss = self.hidden_subset_block(block_num, n)
            if ss:
                return ss
        return None

    # endregion

    # region Fish
    def basic_fish_in_rows(self, y1, y2):
        """
        :param y1: The 1st row number. Precondition: 0 <= y1 < 9
        :param y2: The 2nd row number. Precondition: 0 <= y2 < 9
        Finds a basic fish in rows and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        candidates = self.remaining_in_y[y1].intersection(self.remaining_in_y[y2])
        y1_locs_left = self.locs_left_by_y[y1]
        y2_locs_left = self.locs_left_by_y[y2]
        for candidate in candidates:
            possible_locs = y1_locs_left[candidate]
            if possible_locs == y2_locs_left[candidate] and len(possible_locs) == 2:
                for x in possible_locs:
                    # Make sure there is a candidate worth eliminating
                    if len(self.locs_left_by_x[x][candidate]) > 2:
                        updated_cells = self.eliminate_possibilities_from_col(x, {candidate}, {y1, y2})
                if updated_cells:
                    description = "Basic Fish in Rows: In rows " + str({y1, y2}) + ", candidate " \
                                  + str(candidate) + " can only be placed in cols " + str(possible_locs) \
                                  + ".\nEliminating the candidate from other cells in those cols."
                    return SudokuStep(None, updated_cells, description)
        return None

    def basic_fish_in_cols(self, x1, x2):
        """
        :param x1: The 1st col number. Precondition: 0 <= x1 < 9
        :param x2: The 2nd col number. Precondition: 0 <= x2 < 9
        Finds a basic fish in cols and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        candidates = self.remaining_in_x[x1].intersection(self.remaining_in_x[x2])
        x1_locs_left = self.locs_left_by_x[x1]
        x2_locs_left = self.locs_left_by_x[x2]
        for candidate in candidates:
            possible_locs = x1_locs_left[candidate]
            if possible_locs == x2_locs_left[candidate] and len(possible_locs) == 2:
                for y in possible_locs:
                    # Make sure there is a candidate worth eliminating
                    if len(self.locs_left_by_y[y][candidate]) > 2:
                        updated_cells.update(self.eliminate_possibilities_from_row(y, {candidate}, {x1, x2}))
                if updated_cells:
                    description = "Basic Fish in Cols: In cols " + str({x1, x2}) + ", candidate " \
                                  + str(candidate) + " can only be placed in rows " + str(possible_locs) \
                                  + ".\nEliminating the candidates from other cells in those rows."
                    return SudokuStep(None, updated_cells, description)
        return None

    def perform_basic_fish(self):
        """
        Finds basic fish (size 2) which are also called X-Wings and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for (y1, y2) in itertools.combinations(all_locs, 2):
            ss = self.basic_fish_in_rows(y1, y2)
            if ss:
                return ss
        for (x1, x2) in itertools.combinations(all_locs, 2):
            ss = self.basic_fish_in_cols(x1, x2)
            if ss:
                return ss
        return None

    def fish_in_rows(self, ys):
        """
        :param ys: The row numbers. Precondition: 0 <= y < 9 for y in ys
        Finds a fish in rows and eliminates possibilities accordingly
        A fish of size n (n=len(ys)) in rows is when all potential cells for that candidate in the rows ys
        are contained in n cols total.
        All other occurrences of the candidate in those n cols can be eliminated as a result.
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        n = len(ys)
        candidates = copy.deepcopy(all_possibilities)
        for y in ys:
            candidates.intersection_update(self.remaining_in_y[y])
        for candidate in candidates:
            possible_locs = set()
            for y in ys:
                possible_locs.update(self.locs_left_by_y[y][candidate])
                if len(possible_locs) > n:
                    break
            if len(possible_locs) == n:
                for x in possible_locs:
                    for y_to_remove in self.locs_left_by_x[x][candidate].difference(ys):
                        cell_name = self.board[y_to_remove][x]
                        if self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate):
                            updated_cells.add((cell_name, candidate))
                if updated_cells:
                    description = "Fish " + str(n) + " in Rows: In rows " + str(ys) + ", candidate " \
                                  + str(candidate) + " can only be placed in cols " + str(possible_locs) \
                                  + ".\nEliminating the candidates from other cells in those cols."
                    return SudokuStep(None, updated_cells, description)
        return None

    def fish_in_cols(self, xs):
        """
        :param xs: The col numbers. Precondition: 0 <= x < 9 for x in xs
        Finds a fish in cols and eliminates possibilities accordingly
        A fish of size n (n=len(ys)) in cols is when all potential cells for that candidate in the cols xs
        are contained in n rows total.
        All other occurrences of the candidate in those n rows can be eliminated as a result.
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        n = len(xs)
        candidates = copy.deepcopy(all_possibilities)
        for x in xs:
            candidates.intersection_update(self.remaining_in_x[x])
        for candidate in candidates:
            possible_locs = set()
            for x in xs:
                possible_locs.update(self.locs_left_by_x[x][candidate])
                if len(possible_locs) > n:
                    break
            if len(possible_locs) == n:
                for y in possible_locs:
                    for x_to_remove in self.locs_left_by_y[y][candidate].difference(xs):
                        cell_name = self.board[y][x_to_remove]
                        if self.remove_possibility_from_puzzle_by_cell_name(cell_name, candidate):
                            updated_cells.add((cell_name, candidate))
                if updated_cells:
                    description = "Fish " + str(n) + " in Cols: In cols " + str(xs) + ", candidate " \
                                  + str(candidate) + " can only be placed in rows " + str(possible_locs) \
                                  + ".\nEliminating the candidates from other cells in those rows."
                    return SudokuStep(None, updated_cells, description)
        return updated_cells

    def perform_fish(self, n):
        """
        :param n: The number of rows/cols to search for fish in
        Finds fish (size n) and eliminates possibilities accordingly
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        for ys in itertools.combinations(all_locs, n):
            ss = self.fish_in_rows(set(ys))
            if ss:
                return ss
        for xs in itertools.combinations(all_locs, n):
            ss = self.fish_in_cols(xs)
            if ss:
                return ss
        return None

    # endregion

    # region Skyscraper
    def skyscraper_in_rows(self, val):
        """
        :param val: The candidate to find. Precondition: 1 <= val <= 9
        Finds skyscrapers with the 'base' in a row and eliminates possibilities accordingly.
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        candidate_loc_dict = self.loc_dict_with_len_constraint_for_val(self.locs_left_by_x, val, lambda l: l == 2)
        for (x1, x2) in itertools.combinations(candidate_loc_dict.keys(), 2):
            locs_1 = candidate_loc_dict[x1]
            locs_2 = candidate_loc_dict[x2]
            locs_in_both = locs_1.intersection(locs_2)
            if len(locs_in_both) == 1:
                loc_in_both = next(iter(locs_in_both))
                y1 = next(iter(locs_1.difference(locs_in_both)))
                y2 = next(iter(locs_2.difference(locs_in_both)))
                cell_name_1 = self.board[y1][x1]
                cell_name_2 = self.board[y2][x2]
                cells_seen_by_both = self.get_cell_names_seen_by_both_cells(cell_name_1, cell_name_2)
                for cell_name in cells_seen_by_both:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
                if updated_cells:
                    base_cell_name_1 = self.board[loc_in_both][x1]
                    base_cell_name_2 = self.board[loc_in_both][x2]
                    description = "Skyscraper in Rows: Candidate " + str(val) + " only has two remaining cells " \
                                  "for cols " + str({x1, x2}) + \
                                  "\nFurthermore, the two 'Base' cells: "\
                                  + str({base_cell_name_1, base_cell_name_2}) \
                                  + " are both in row " + str(loc_in_both) + "."\
                                  + "\nThus, we can eliminate the candidate from all cells seen by both 'Tower' " \
                                    "cells: " + str({cell_name_1, cell_name_2}) + "."
                    return SudokuStep(None, updated_cells, description)
        return None

    def skyscraper_in_cols(self, val):
        """
        :param val: The candidate to find. Precondition: 1 <= val <= 9
        Finds skyscrapers with the 'base' in a col and eliminates possibilities accordingly.
        :return A SudokuStep corresponding to the guess where:
                * updated_cells = A set of (cell name, candidate) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        candidate_loc_dict = self.loc_dict_with_len_constraint_for_val(self.locs_left_by_y, val, lambda l: l == 2)
        for (y1, y2) in itertools.combinations(candidate_loc_dict.keys(), 2):
            locs_1 = candidate_loc_dict[y1]
            locs_2 = candidate_loc_dict[y2]
            locs_in_both = locs_1.intersection(locs_2)
            if len(locs_in_both) == 1:
                loc_in_both = next(iter(locs_in_both))
                x1 = next(iter(locs_1.difference(locs_in_both)))
                x2 = next(iter(locs_2.difference(locs_in_both)))
                cell_name_1 = self.board[y1][x1]
                cell_name_2 = self.board[y2][x2]
                cells_seen_by_both = self.get_cell_names_seen_by_both_cells(cell_name_1, cell_name_2)
                for cell_name in cells_seen_by_both:
                    if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                        updated_cells.add((cell_name, val))
                if updated_cells:
                    base_cell_name_1 = self.board[y1][loc_in_both]
                    base_cell_name_2 = self.board[y2][loc_in_both]
                    description = "Skyscraper in Cols: Candidate " + str(val) + " only has two remaining cells " \
                                  "for rows " + str({y1, y2}) + \
                                  "\nFurthermore, the two 'Base' cells: "\
                                  + str({base_cell_name_1, base_cell_name_2}) \
                                  + " are both in col " + str(loc_in_both) + "."\
                                  + "\nThus, we can eliminate the candidate from all cells seen by both 'Tower' " \
                                    "cells: " + str({cell_name_1, cell_name_2}) + "."
                    return SudokuStep(None, updated_cells, description)
        return None

    def perform_skyscraper(self):
        for candidate in all_possibilities:
            ss = self.skyscraper_in_rows(candidate)
            if ss:
                return ss
        for candidate in all_possibilities:
            ss = self.skyscraper_in_cols(candidate)
            if ss:
                return ss

    # endregion

    @staticmethod
    def loc_dict_with_len_constraint_for_val(locs_left_by, val, len_lambda):
        """
        :param locs_left_by: locs_left_by[offset][val] should contain a set with all occurrences of val in the
        Row/Col/Block
        :param val: The candidate to find in locs_left_by. Precondition: 1 <= val <= 9
        :param len_lambda: The lambda function to execute of the length of each possibility.
        Should be a function that takes in a length and returns true/false
        :return: A dictionary with:
        Key: Offset within a row/col/block.
        Value: A set containing all possible locs for that val
        where the length of the set satisfies the supplied lambda
        """
        return {o: locs_left_by[o][val] for o in all_locs if len_lambda(len(locs_left_by[o][val]))}

    def get_cell_names_seen_by_both_cells(self, cell_name_1, cell_name_2):
        """
        :param cell_name_1: The name of the 1st cell
        :param cell_name_2: The name of the 2nd cell
        :return: The names of all cells that can be seen by both cells
        """
        cell_1 = self.cells_dict[cell_name_1]
        seen_by_1 = set()
        seen_by_1.update(self.y_cell_list[cell_1.y])
        seen_by_1.update(self.x_cell_list[cell_1.x])
        seen_by_1.update(self.block_cell_list[cell_1.block])
        cell_2 = self.cells_dict[cell_name_2]
        seen_by_2 = set()
        seen_by_2.update(self.y_cell_list[cell_2.y])
        seen_by_2.update(self.x_cell_list[cell_2.x])
        seen_by_2.update(self.block_cell_list[cell_2.block])
        # Get the cells in the intersection of the cells seen by each
        cells_seen_by_both = seen_by_1.intersection(seen_by_2)
        cells_seen_by_both.difference_update({cell_name_1, cell_name_2})
        return cells_seen_by_both

    # region Kite
    def kite(self, val):
        """
        :param val: The candidate to find. Precondition: 1 <= val <= 9
        Finds kites with the candidate and eliminates possibilities accordingly.
        :return A set of (cell name, removed possibility) tuples for the cells with possibilities removed
        """
        updated_cells = set()
        candidate_loc_dict_y = self.loc_dict_with_len_constraint_for_val(self.locs_left_by_y, val, lambda l: l == 2)
        candidate_loc_dict_x = self.loc_dict_with_len_constraint_for_val(self.locs_left_by_x, val, lambda l: l == 2)

        y_block_num_cell_dict = defaultdict(set)
        x_block_num_cell_dict = defaultdict(set)
        for y, locs in candidate_loc_dict_y.items():
            for x in locs:
                cell = self.cells_dict[self.board[y][x]]
                y_block_num_cell_dict[cell.block].add(cell)
        for x, locs in candidate_loc_dict_x.items():
            for y in locs:
                cell = self.cells_dict[self.board[y][x]]
                x_block_num_cell_dict[cell.block].add(cell)

        # If any of the cells from the y_loc_dict are in the same block num as one from the x_loc_dict
        shared_block_nums = set(y_block_num_cell_dict.keys()).intersection(set(x_block_num_cell_dict.keys()))
        for block_num in shared_block_nums:
            y_cells = y_block_num_cell_dict[block_num]
            x_cells = x_block_num_cell_dict[block_num]
            for y_cell in y_cells:
                x = next(iter(candidate_loc_dict_y[y_cell.y].difference({y_cell.x})))
                for x_cell in x_cells:
                    if y_cell.y != x_cell.y and y_cell.x != x_cell.x:
                        y = next(iter(candidate_loc_dict_x[x_cell.x].difference({x_cell.y})))
                        cell_name = self.board[y][x]
                        if self.remove_possibility_from_puzzle_by_cell_name(cell_name, val):
                            updated_cells.add((cell_name, val))
                            horizontal_kite = {self.board[y_cell.y][x], y_cell.name}
                            vertical_kite = {self.board[y][x_cell.x], x_cell.name}
                            description = "Kite: Candidate " + str(val) + " has two strings: " \
                                          + "\nRow " + str(y_cell.y) + ": " + str(horizontal_kite) \
                                          + "\nCol " + str(x_cell.x) + ": " + str(vertical_kite) \
                                          + "\nThe bases of these strings share block " + str(block_num) \
                                          + ". Thus, we can eliminate the candidate from cells that see the other " \
                                            "two ends of the string."
                            return SudokuStep(None, updated_cells, description)
        return None

    def perform_kite(self):
        for candidate in all_possibilities:
            ss = self.kite(candidate)
            if ss:
                return ss

    # endregion

    # region Enumerate Possibilities
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
    # endregion

    # region Pretty Print
    @staticmethod
    def print_matrix(matrix):
        """
        :param matrix: A 9x9 2D-matrix with contents to pretty print
        Pretty prints the values in the matrix
        """
        print(SudokuPuzzle.get_pretty_matrix_string(matrix))

    @staticmethod
    def get_pretty_matrix_string(matrix):
        """
        :param: A 9x9 2D-matrix with contents
        :return Returns the contents of the matrix as a prettified string
        """
        s = ""
        row_count = 0
        col_count = 0
        for y in all_locs:
            if row_count % 3 == 0:
                row_count = 0
                s += '+-----------------------------+\n'
            row_count += 1
            for x in all_locs:
                val = matrix[y][x]
                if col_count % 3 == 0:
                    col_count = 0
                    s += '|'
                col_count += 1
                if val is None:
                    s += '   '
                else:
                    s += ' ' + str(val) + ' '
            s += '|\n'
        s += '+-----------------------------+'
        return s

    def print_possibilities(self):
        SudokuPuzzle.print_matrix(self.get_possibilities())

    def print_board(self):
        SudokuPuzzle.print_matrix(self.get_board())

    def get_pretty_possibilities_string(self):
        SudokuPuzzle.get_pretty_matrix_string(self.get_possibilities())

    def get_pretty_board_string(self):
        SudokuPuzzle.get_pretty_matrix_string(self.get_board())

    # region Validation
    def validate_board(self):
        """
        :return: A list of cells which break at least one sudoku rule
        """
        illegal_cells = set()
        # Check row condition
        cell_names_by_candidate = {candidate: set() for candidate in all_possibilities}
        for cell_name, cell in self.cells_dict.items():
            if cell.val is not None:
                cell_names_by_candidate[cell.val].add(cell_name)

        for candidate in all_possibilities:
            for (c1, c2) in itertools.combinations(cell_names_by_candidate[candidate], 2):
                cell_1 = self.cells_dict[c1]
                cell_2 = self.cells_dict[c2]
                if cell_1.y == cell_2.y or cell_1.x == cell_2.x or cell_1.block == cell_2.block:
                    illegal_cells.add(c1)
                    illegal_cells.add(c2)
        return illegal_cells

    # endregion

    # region Rotate/Reflect Board
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
    # endregion

    # End file
