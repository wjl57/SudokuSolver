import copy
import unittest
from SudokuError import BadGuessError
from SudokuError import BadPuzzleError
from SudokuPuzzle import SudokuPuzzle
from SudokuHelper import all_locs
from SudokuHelper import all_possibilities

__author__ = 'william'


class TestSudokuPuzzle(unittest.TestCase):

    ###############################################################################################################
    # Test Boards
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://hodoku.sourceforge.net/en/
    ###############################################################################################################
    # region

    def get_board_copy(self, board):
        return copy.deepcopy(board)

    # region Empty board
    empty_board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]
    # endregion

    # region Test board
    test_board = [
        [4, None, 2, None, 3, 1, 7, 6, None],
        [None, 6, None, None, 8, 7, None, None, None],
        [None, None, None, None, 4, None, 1, None, None],
        [8, 9, None, None, None, 2, 6, None, 3],
        [3, None, 5, None, None, None, 4, None, 1],
        [1, None, 6, 3, None, None, None, 8, 5],
        [None, None, 8, None, 9, None, None, None, None],
        [None, None, None, 4, 2, None, None, 5, None],
        [None, 4, 9, 7, 5, None, 3, None, 6]
    ]
    # endregion

    # region Guess boards
    guess_board = [
        [1, 2, 3, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    missing_candidate_validation_board = [
        [1, None, None, None, None, None, None, None, None],
        [None, None, None, 1, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, 1, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, 1, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    empty_possibilities_validation_board = [
        [None, None, None, None, None, None, None, None, 6],
        [None, None, None, None, None, None, None, None, 7],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [1, 2, 3, 4, 5, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    # region Sole and unique candidate boards
    sole_candidate_board = [
        [None, None, None, None, None, 1, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, 6, None, None, None],
        [None, None, None, 4, None, None, None, None, None],
        [None, None, None, None, 8, None, None, None, None],
        [2, None, 9, None, None, None, None, None, 7],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, 3, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    unique_candidate_board = [
        [1, 2, 3, None, None, None, None, None, 9],
        [None, None, None, 4, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, 4, None, None]
    ]

    unique_candidate_block_board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, 5, None, None, None],
        [None, None, None, None, None, None, None, None, 4],
        [None, None, None, 4, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, 4, None, None, None, None]
    ]
    # endregion

    # region Block+row/column/block boards
    block_rc_board = [
        [None, None, None, None, 7, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, 2, None, 1, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, 9, None, 6, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    block_block_board = [
        [None, None, None, None, None, None, None, None, None],
        [None, None, 8, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [2, 9, None, None, 1, 4, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, 8, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]
    # endregion

    # region Naked tuple boards
    naked_pair_board = [
        [None, 2, None, 1, None, None, None, None, None],
        [None, None, 6, None, None, None, None, None, None],
        [5, None, 3, None, None, None, None, None, None],
        [None, 3, None, None, None, None, None, None, None],
        [None, 1, None, None, 2, None, 6, None, None],
        [None, None, None, 6, None, None, None, None, None],
        [8, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [9, None, None, None, None, None, None, None, None]
    ]

    naked_pair_block_board = [
        [None, None, None, None, None, 4, None, None, None],
        [None, None, None, None, None, 2, None, None, None],
        [None, None, None, 3, 5, 6, None, None, None],
        [3, 1, None, None, None, 7, 2, 4, 6],
        [7, 6, None, None, None, None, 3, None, 5],
        [None, 2, None, None, None, None, 7, None, 1],
        [None, None, None, None, None, 1, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    naked_triple_board = [
        [None, None, None, 2, 9, 4, 3, 8, None],
        [None, None, None, 1, 7, 8, 6, 4, None],
        [4, 8, None, 3, 5, 6, 1, None, None],
        [None, None, None, 8, 3, 7, 5, None, 1],
        [None, None, None, 4, 1, 5, 7, None, None],
        [None, None, None, 6, 2, 9, 8, 3, 4],
        [9, 5, 3, None, None, None, None, None, None],
        [1, 2, 6, None, None, None, None, None, None],
        [None, 4, None, None, None, None, None, None, None]
    ]

    naked_triple_block_board = [
        [3, 9, None, None, None, None, 7, None, None],
        [None, None, None, None, None, None, 6, 5, None],
        [5, None, 7, None, None, None, 3, 4, 9],
        [None, None, None, 3, 8, None, None, None, None],
        [None, None, None, None, 5, 4, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, 8, None, None, None, None, None],
        [None, None, None, 9, 4, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]

    naked_quad_block_board = [
        [5, 3, 2, None, None, None, None, None, None],
        [9, 7, 8, None, None, None, None, None, None],
        [None, None, 1, None, None, None, None, None, None],
        [None, 2, 5, None, None, None, None, None, None],
        [None, None, 3, None, None, None, None, None, None],
        [7, None, None, None, None, None, None, None, None],
        [None, None, None, 1, None, None, None, None, None],
        [None, None, None, 8, None, 5, 1, None, 6],
        [None, None, None, 3, None, None, None, 9, 8]
    ]

    naked_quad_board = [
        [None, 1, None, 7, 2, None, 5, 6, 3],
        [None, 5, 6, None, 3, None, 2, 4, 7],
        [7, 3, 2, 5, 4, 6, 1, 8, 9],
        [6, 9, 3, 2, 8, 7, 4, 1, 5],
        [2, 4, 7, 6, 1, 5, 9, 3, 8],
        [5, 8, 1, 3, 9, 4, None, None, None],
        [None, None, None, None, None, 2, None, None, None],
        [None, None, None, None, None, None, None, None, 1],
        [None, None, 5, 8, 7, None, None, None, None]
    ]
    # endregion

    # region Hidden subset boards
    hidden_pair_board = [
        [None, 4, 9, 1, 3, 2, None, None, None],
        [None, 8, 1, 4, 7, 9, None, None, None],
        [3, 2, 7, 6, 8, 5, 9, 1, 4],
        [None, 9, 6, None, 5, 1, 8, None, None],
        [None, 7, 5, None, 2, 8, None, None, None],
        [None, 3, 8, None, 4, 6, None, None, 5],
        [8, 5, 3, 2, 6, 7, None, None, None],
        [7, 1, 2, 8, 9, 4, 5, 6, 3],
        [9, 6, 4, 5, 1, 3, None, None, None]
    ]

    hidden_pair_block_board = [
        [None, None, None, None, 6, None, None, None, None],
        [None, None, None, None, 4, 2, 7, 3, 6],
        [None, None, 6, 7, 3, None, None, 4, None],
        [None, 9, 4, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [6, None, 7, None, None, None, None, None, None],
        [1, None, None, None, None, None, None, None, None],
        [None, 6, None, None, None, None, None, None, None],
        [None, None, 5, None, None, None, None, None, None]
    ]

    hidden_triple_board = [
        [5, None, None, 6, 2, None, None, 3, 7],
        [None, None, 4, 8, 9, None, None, None, None],
        [None, None, None, None, 5, None, None, None, None],
        [9, 3, None, None, None, None, None, None, None],
        [None, 2, None, None, None, None, 6, None, 5],
        [7, None, None, None, None, None, None, None, 3],
        [None, None, None, None, None, 9, None, None, None],
        [None, None, None, None, None, None, 7, None, None],
        [6, 8, None, 5, 7, None, None, None, 2]
    ]

    hidden_triple_block_board = [
        [2, 8, None, None, None, None, 4, 7, 3],
        [5, 3, 4, 8, 2, 7, 1, 9, 6],
        [None, 7, 1, None, 3, 4, None, 8, None],
        [3, None, None, 5, None, None, None, 4, None],
        [None, None, None, 3, 4, None, None, 6, None],
        [4, 6, None, 7, 9, None, 3, 1, None],
        [None, 9, None, 2, None, 3, 6, 5, 4],
        [None, None, 3, None, None, 9, 8, 2, 1],
        [None, None, None, None, 8, None, 9, 3, 7]
    ]
    # endregion

    # region Fish boards
    basic_fish_row_board = [
        [None, 4, 1, 7, 2, 9, None, 3, None],
        [7, 6, 9, None, None, 3, 4, None, 2],
        [None, 3, 2, 6, 4, None, 7, 1, 9],
        [4, None, 3, 9, None, None, 1, 7, None],
        [6, None, 7, None, None, 4, 9, None, 3],
        [1, 9, 5, 3, 7, None, None, 2, 4],
        [2, 1, 4, 5, 6, 7, 3, 9, 8],
        [3, 7, 6, None, 9, None, 5, 4, 1],
        [9, 5, 8, 4, 3, 1, 2, 6, 7]
    ]

    basic_fish_col_board = [
        [9, 8, None, None, 6, 2, 7, 5, 3],
        [None, 6, 5, None, None, 3, None, None, None],
        [3, 2, 7, None, 5, None, None, None, 6],
        [7, 9, None, None, 3, None, 5, None, None],
        [None, 5, None, None, None, 9, None, None, None],
        [8, 3, 2, None, 4, 5, None, None, 9],
        [6, 7, 3, 5, 9, 1, 4, 2, 8],
        [2, 4, 9, None, 8, 7, None, None, 5],
        [5, 1, 8, None, 2, None, None, None, 7]
    ]

    fish_3_row_board = [
        [1, 6, None, 5, 4, 3, None, 7, None],
        [None, 7, 8, 6, None, 1, 4, 3, 5],
        [4, 3, 5, 8, None, 7, 6, None, 1],
        [7, 2, None, 4, 5, 8, None, 6, 9],
        [6, None, None, 9, 1, 2, None, 5, 7],
        [None, None, None, 3, 7, 6, None, None, 4],
        [None, 1, 6, None, 3, None, None, 4, None],
        [3, None, None, None, 8, None, None, 1, 6],
        [None, None, 7, 1, 6, 4, 5, None, 3]
    ]

    fish_3_row_board_2 = [
        [1, None, 8, 5, None, None, 2, 3, 4],
        [5, None, None, 3, None, 2, 1, 7, 8],
        [None, None, None, 8, None, None, 5, 6, 9],
        [8, None, None, 6, None, 5, 7, 9, 3],
        [None, None, 5, 9, None, None, 4, 8, 1],
        [3, None, None, None, None, 8, 6, 5, 2],
        [9, 8, None, 2, None, 6, 3, 1, None],
        [None, None, None, None, None, None, 8, None, None],
        [None, None, None, 7, 8, None, 9, None, None]
    ]

    fish_4_row_board = [
        [2, None, None, None, None, None, None, None, 3],
        [None, 8, None, None, 3, None, None, 5, None],
        [None, None, 3, 4, None, 2, 1, None, None],
        [None, None, 1, 2, None, 5, 4, None, None],
        [None, None, None, None, 9, None, None, None, None],
        [None, None, 9, 3, None, 8, 6, None, None],
        [None, None, 2, 5, None, 6, 9, None, None],
        [None, 9, None, None, 2, None, None, 7, None],
        [4, None, None, None, None, None, None, None, 1]
    ]
    # endregion

    # region Single digit pattern boards
    skyscraper_row_board = [
        [6, 9, 7, None, None, None, None, None, 2],
        [None, None, 1, 9, 7, 2, None, 6, 3],
        [None, None, 3, None, None, 6, 7, 9, None],
        [9, 1, 2, None, None, None, 6, None, 7],
        [3, 7, 4, 2, 6, None, 9, 5, None],
        [8, 6, 5, 7, None, 9, None, 2, 4],
        [1, 4, 8, 6, 9, 3, 2, 7, 5],
        [7, None, 9, None, 2, 4, None, None, 6],
        [None, None, 6, 8, None, 7, None, None, 9]
    ]

    skyscraper_col_board = [
        [None, None, 1, None, 2, 8, 7, 5, 9],
        [None, 8, 7, 9, None, 5, 1, 3, 2],
        [9, 5, 2, 1, 7, 3, 4, 8, 6],
        [None, 2, None, 7, None, None, 3, 4, None],
        [None, None, None, 5, None, None, 2, 7, None],
        [7, 1, 4, 8, 3, 2, 6, 9, 5],
        [None, None, None, None, 9, None, 8, 1, 7],
        [None, 7, 8, None, 5, 1, 9, 6, 3],
        [1, 9, None, None, 8, 7, 5, 2, 4]
    ]

    kite_board = [
        [None, 8, 1, None, 2, None, 6, None, None],
        [None, 4, 2, None, 6, None, None, 8, 9],
        [None, 5, 6, 8, None, None, 2, 4, None],
        [6, 9, 3, 1, 4, 2, 7, 5, 8],
        [4, 2, 8, 3, 5, 7, 9, 1, 6],
        [1, 7, 5, 6, 8, 9, 3, 2, 4],
        [5, 1, None, None, 3, 6, 8, 9, 2],
        [2, 3, None, None, None, 8, 4, 6, None],
        [8, 6, None, 2, None, None, None, None, None]
    ]

    dual_kite_board = [
        [3, 2, None, 5, 4, 7, 9, None, 6],
        [None, None, 6, 2, 1, 3, None, 5, None],
        [None, 4, 5, 6, 9, 8, 2, 3, None],
        [5, None, None, 4, 7, 2, None, None, None],
        [None, None, 7, 9, None, 1, None, 2, 5],
        [None, None, 2, 8, None, 5, 7, None, None],
        [2, 1, 4, 3, 5, 9, 6, 7, 8],
        [6, 7, 3, 1, 8, 4, 5, 9, 2],
        [None, 5, None, 7, 2, 6, 1, 4, 3]
    ]
    # endregion

    # region Validation boards
    illegal_puzzle_board = [
        [2, 1, None, None, None, None, None, None, 2],
        [None, None, 2, None, None, None, None, None, None],
        [4, None, None, None, None, None, None, None, None],
        [1, None, None, None, 4, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, 2, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None]
    ]
    # endregion

    # region Rotation boards
    rotation_board = [
        [1, 2, None, None, None, None, None, None, 3],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, 6, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, 7, None, None, None],
        [4, None, None, None, None, None, None, None, 8]
    ]
    # endregion

    # endregion
    ###############################################################################################################
    # Constructor tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region
    def test_init_possibilities(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        board = sp.get_board()
        self.assertListEqual(board, self.get_board_copy(self.test_board))

        expected_possibilities = [
            [{4}, {8, 5}, {2}, {9, 5}, {3}, {1}, {7}, {6}, {8, 9}],
            [{9, 5}, {6}, {1, 3}, {9, 2, 5}, {8}, {7}, {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}],
            [{9, 5, 7}, {8, 3, 5, 7}, {3, 7}, {9, 2, 5, 6}, {4}, {9, 5, 6}, {1}, {9, 2, 3}, {8, 9, 2}],
            [{8}, {9}, {4, 7}, {1, 5}, {1, 7}, {2}, {6}, {7}, {3}],
            [{3}, {2, 7}, {5}, {8, 9, 6}, {6, 7}, {8, 9, 6}, {4}, {9, 2, 7}, {1}],
            [{1}, {2, 7}, {6}, {3}, {7}, {9, 4}, {9, 2}, {8}, {5}],
            [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, {8}, {1, 6}, {9}, {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}],
            [{6, 7}, {1, 3, 7}, {1, 3, 7}, {4}, {2}, {8, 3, 6}, {8, 9}, {5}, {8, 9, 7}],
            [{2}, {4}, {9}, {7}, {5}, {8}, {3}, {1, 2}, {6}]
        ]
        p = sp.get_possibilities()
        self.assertListEqual(p, expected_possibilities)

    def test_init_remaining_in(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        expected_remaining_in_y = [
            {5, 8, 9}, {1, 2, 3, 4, 5, 9}, {2, 3, 5, 6, 7, 8, 9},
            {1, 4, 5, 7}, {2, 6, 7, 8, 9}, {2, 4, 7, 9},
            {1, 2, 3, 4, 5, 6, 7}, {1, 3, 6, 7, 8, 9}, {1, 2, 8}
        ]
        self.assertListEqual(sp.remaining_in_y, expected_remaining_in_y)

        expected_remaining_in_x = [
            {2, 5, 6, 7, 9}, {1, 2, 3, 5, 7, 8}, {1, 3, 4, 7},
            {1, 2, 5, 6, 8, 9}, {1, 6, 7}, {3, 4, 5, 6, 8, 9},
            {2, 5, 8, 9}, {1, 2, 3, 4, 7, 9}, {2, 4, 7, 8, 9}
        ]
        self.assertListEqual(sp.remaining_in_x, expected_remaining_in_x)

        expected_remaining_in_blocks = [
            {1, 3, 5, 7, 8, 9}, {2, 5, 6, 9}, {2, 3, 4, 5, 8, 9},
            {2, 4, 7}, {1, 4, 5, 6, 7, 8, 9}, {2, 7, 9},
            {1, 2, 3, 5, 6, 7}, {1, 3, 6, 8}, {1, 2, 4, 7, 8, 9}
        ]
        self.assertListEqual(sp.remaining_in_blocks, expected_remaining_in_blocks)

    def test_init_locs_left_by(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        expected_possibilities = [
            [{4}, {8, 5}, {2}, {9, 5}, {3}, {1}, {7}, {6}, {8, 9}],
            [{9, 5}, {6}, {1, 3}, {9, 2, 5}, {8}, {7}, {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}],
            [{9, 5, 7}, {8, 3, 5, 7}, {3, 7}, {9, 2, 5, 6}, {4}, {9, 5, 6}, {1}, {9, 2, 3}, {8, 9, 2}],
            [{8}, {9}, {4, 7}, {1, 5}, {1, 7}, {2}, {6}, {7}, {3}],
            [{3}, {2, 7}, {5}, {8, 9, 6}, {6, 7}, {8, 9, 6}, {4}, {9, 2, 7}, {1}],
            [{1}, {2, 7}, {6}, {3}, {7}, {9, 4}, {9, 2}, {8}, {5}],
            [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, {8}, {1, 6}, {9}, {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}],
            [{6, 7}, {1, 3, 7}, {1, 3, 7}, {4}, {2}, {8, 3, 6}, {8, 9}, {5}, {8, 9, 7}],
            [{2}, {4}, {9}, {7}, {5}, {8}, {3}, {1, 2}, {6}]
        ]
        p = sp.get_possibilities()

        self.assertListEqual(p, expected_possibilities)

        expected_locs_left_by_y_0 = {1: {5}, 2: {2}, 3: {4}, 4: {0}, 5: {1, 3},
                                     6: {7}, 7: {6}, 8: {1, 8}, 9: {3, 8}}
        expected_locs_left_by_y_1 = {1: {2}, 2: {3, 6, 7, 8}, 3: {2, 7}, 4: {7, 8}, 5: {0, 3, 6},
                                     6: {1}, 7: {5}, 8: {4}, 9: {0, 3, 6, 7, 8}}
        self.assertDictEqual(sp.locs_left_by_y[0], expected_locs_left_by_y_0)
        self.assertDictEqual(sp.locs_left_by_y[1], expected_locs_left_by_y_1)

        expected_locs_left_by_x_0 = {1: {5}, 2: {6, 8}, 3: {4}, 4: {0}, 5: {1, 2, 6},
                                     6: {6, 7}, 7: {2, 6, 7}, 8: {3}, 9: {1, 2}}
        expected_locs_left_by_x_1 = {1: {6, 7}, 2: {4, 5, 6}, 3: {2, 6, 7}, 4: {8}, 5: {0, 2, 6},
                                     6: {1}, 7: {2, 4, 5, 6, 7}, 8: {0, 2}, 9: {3}}
        self.assertDictEqual(sp.locs_left_by_x[0], expected_locs_left_by_x_0)
        self.assertDictEqual(sp.locs_left_by_x[1], expected_locs_left_by_x_1)

        expected_locs_left_by_block_0 = {1: {5}, 2: {2}, 3: {5, 7, 8}, 4: {0}, 5: {1, 3, 6, 7},
                                         6: {4}, 7: {6, 7, 8}, 8: {1, 7}, 9: {3, 6}}
        expected_locs_left_by_block_7 = {1: {0}, 2: {4}, 3: {2, 5}, 4: {3}, 5: {7},
                                         6: {0, 2, 5}, 7: {6}, 8: {5, 8}, 9: {1}}

        self.assertDictEqual(sp.locs_left_by_block[0], expected_locs_left_by_block_0)
        self.assertDictEqual(sp.locs_left_by_block[7], expected_locs_left_by_block_7)

    # endregion
    ###############################################################################################################
    # Enumerate candidates tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region
    def test_enumerate_possibilities_by_row(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        row_1_possibilities = sp.enumerate_row_possibilities(1)
        self.assertListEqual(row_1_possibilities,
                             [{9, 5}, {6}, {1, 3}, {9, 2, 5}, {8}, {7}, {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}])
        row_6_possibilities = sp.enumerate_row_possibilities(6)
        self.assertListEqual(row_6_possibilities,
                             [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, {8}, {1, 6}, {9}, {3, 6}, {2}, {1, 2, 4, 7},
                              {2, 4, 7}])

    def test_enumerate_possibilities_by_col(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        col_1_possibilities = sp.enumerate_col_possibilities(1)
        self.assertListEqual(col_1_possibilities, [{8, 5}, {6}, {8, 3, 5, 7}, {9}, {2, 7},
                                                   {2, 7}, {1, 2, 3, 5, 7}, {1, 3, 7}, {4}])
        col_6_possibilities = sp.enumerate_col_possibilities(6)
        self.assertListEqual(col_6_possibilities, [{7}, {9, 2, 5}, {1}, {6}, {4},
                                                   {9, 2}, {2}, {8, 9}, {3}])

    def test_enumerate_possibilities_by_block(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        block_1_possibilities = sp.enumerate_block_possibilities(1)
        self.assertListEqual(block_1_possibilities,
                             [{9, 5}, {3}, {1}, {9, 2, 5}, {8}, {7}, {9, 2, 5, 6}, {4}, {9, 5, 6}])
        block_6_possibilities = sp.enumerate_block_possibilities(6)
        self.assertListEqual(block_6_possibilities, [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, {8}, {6, 7},
                                                     {1, 3, 7}, {1, 3, 7}, {2}, {4}, {9}])
    # endregion
    ###############################################################################################################
    # Sole candidate tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_fill_sole_candidates(self):
        sp = SudokuPuzzle(self.get_board_copy(self.sole_candidate_board))
        (y, x) = (5, 5)
        cell = sp.cells_dict[sp.board[y][x]]
        self.assertEqual(cell.val, None)
        sp.fill_sole_candidate()
        cell = sp.cells_dict[sp.board[y][x]]
        self.assertEqual(cell.val, 5)
        self.assertSetEqual(sp.get_possibilities()[y][x], {5})

    # endregion
    ###############################################################################################################
    # Unique candidate tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_fill_unique_candidates(self):
        sp = SudokuPuzzle(self.get_board_copy(self.unique_candidate_board))
        (cell_y, cell_x) = (0, 7)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidate_y(0)
        self.assertEqual(cell.val, 4)

        sp = SudokuPuzzle(SudokuPuzzle.reflect_board_over_xy(self.get_board_copy(self.unique_candidate_board)))
        (cell_y, cell_x) = (7, 0)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidate_x(0)
        self.assertEqual(cell.val, 4)

        sp = SudokuPuzzle(self.get_board_copy(self.unique_candidate_block_board))
        (cell_y, cell_x) = (0, 5)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidate()
        self.assertEqual(cell.val, 4)

    # endregion
    ###############################################################################################################
    # Helper methods for block row/column interactions
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_find_unique_offsets_for_block_num_and_val(self):
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({0}), ({0}, {0}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({5}), ({1}, {2}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({0, 1, 2}), ({0}, {0, 1, 2}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({0, 2, 3}), ({0, 1}, {0, 2}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({1, 4, 7}), ({0, 1, 2}, {1}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({1, 2, 4, 7}), ({0, 1, 2}, {1, 2}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({1, 2, 3, 4, 5, 6, 7}), ({0, 1, 2}, {0, 1, 2}))
        self.assertEqual(SudokuPuzzle.find_unique_offsets_for_cell_nums({0, 1, 2, 6, 7, 8}), ({0, 2}, {0, 1, 2}))

    def test_remove_possibilities_not_in_block_with_y_offset(self):
        sp = SudokuPuzzle(self.get_board_copy(self.empty_board))
        sp.remove_possibility_not_in_block_with_y_offset(3, 2, 4)
        y = 5
        val = 4
        should_contain = [True, True, True, False, False, False, False, False, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain, row_possibilities, {val})

    def test_remove_possibilities_not_in_block_with_x_offset(self):
        sp = SudokuPuzzle(self.get_board_copy(self.empty_board))
        sp.remove_possibility_not_in_block_with_x_offset(3, 2, 4)
        x = 2
        val = 4
        should_contain = [False, False, False, True, True, True, False, False, False]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain(should_contain, col_possibilities, {val})

    ###############################################################################################################
    # Block row/column interaction tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################

    def test_block_rc_interaction(self):
        sp = SudokuPuzzle(self.get_board_copy(self.block_rc_board))
        y = 4
        val = 7
        # Shouldn't do anything
        sp.block_rc_interaction(1)
        should_contain = [True, True, True, True, False, True, True, True, True]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain, row_possibilities, {val})
        # Should eliminate 6 possibilities
        sp.block_rc_interaction(4)
        should_contain = [False, False, False, True, False, True, False, False, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain, row_possibilities, {val})

    def test_all_block_rc_interactions(self):
        sp = SudokuPuzzle(self.get_board_copy(self.block_rc_board))
        y = 4
        val = 7
        sp.perform_block_rc_interaction()
        should_contain = [False, False, False, True, False, True, False, False, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain, row_possibilities, {val})

    # endregion
    ###############################################################################################################
    # Block block interaction tests
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_block_block_horizontal_interaction(self):
        sp = SudokuPuzzle(self.get_board_copy(self.block_block_board))
        excluded_block_num = 5
        val = 8
        should_contain_before = [True, True, True, True, True, True, True, True, True]
        block_possibilities = sp.enumerate_block_possibilities(excluded_block_num)
        self.assert_should_contain(should_contain_before, block_possibilities, {val})
        sp.block_block_interaction_horizontal(excluded_block_num)
        should_contain_after = [False, False, False, True, True, True, False, False, False]
        block_possibilities = sp.enumerate_block_possibilities(excluded_block_num)
        self.assert_should_contain(should_contain_after, block_possibilities, {val})

    def test_block_block_vertical_interaction(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.block_block_board)))
        excluded_block_num = 7
        val = 8
        should_contain_before = [True, True, True, True, True, True, True, True, True]
        block_possibilities = sp.enumerate_block_possibilities(excluded_block_num)
        self.assert_should_contain(should_contain_before, block_possibilities, {val})
        sp.block_block_interaction_vertical(excluded_block_num)
        should_contain_after = [False, True, False, False, True, False, False, True, False]
        block_possibilities = sp.enumerate_block_possibilities(excluded_block_num)
        self.assert_should_contain(should_contain_after, block_possibilities, {val})

    ###############################################################################################################
    # Naked pair/tuple helper method tests
    # http://hodoku.sourceforge.net/en/tech_naked.php
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################

    def test_get_naked_pairs_in_possibilities_dict(self):
        possibility_dict = {0: [4, 7], 1: [2, 3], 3: [2, 3], 6: [4, 7], 7: [], 8: [0, 7], 9: [2, 3]}
        naked_pair_vals = SudokuPuzzle.get_naked_pair_vals_in_possibilities_dict(possibility_dict)
        offsets = [npv[0] for npv in naked_pair_vals]
        vals = [npv[1] for npv in naked_pair_vals]
        expected_offsets = [(0, 6), (1, 3), (1, 9), (3, 9)]
        expected_vals = [[4, 7], [2, 3], [2, 3], [2, 3]]
        expected_naked_pair_vals = [x for x in zip(expected_offsets, expected_vals)]
        self.assertListEqual(offsets, expected_offsets)
        self.assertListEqual(vals, expected_vals)
        self.assertListEqual(naked_pair_vals, expected_naked_pair_vals)

    def test_get_naked_tuples_in_possibilities_dict(self):
        possibilities_dict = {0: [2, 5], 1: [1, 2, 5], 3: [3, 4, 5, 7, 8], 7: [1, 5], 8: [4, 5, 6, 7]}
        naked_tuple_vals = SudokuPuzzle.get_naked_tuple_vals_in_possibilities_dict(possibilities_dict, 3)
        offsets = [ntv[0] for ntv in naked_tuple_vals]
        vals = [ntv[1] for ntv in naked_tuple_vals]
        expected_offsets = [(0, 1, 7)]
        expected_vals = [{1, 2, 5}]
        expected_naked_tuple_vals = [x for x in zip(expected_offsets, expected_vals)]
        self.assertListEqual(offsets, expected_offsets)
        self.assertListEqual(vals, expected_vals)
        self.assertListEqual(naked_tuple_vals, expected_naked_tuple_vals)

    # endregion
    ###############################################################################################################
    # Naked pair tests
    # http://hodoku.sourceforge.net/en/tech_naked.php
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_naked_pair_y(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.naked_pair_board)))
        vals = {4, 7}
        y = 0
        should_contain_before = [True, True, False, True, True, True, False, True, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain_before, row_possibilities, vals)
        sp.naked_pair_y(y)
        should_contain_after = [True, False, False, False, True, False, False, False, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain_after, row_possibilities, vals)

    def test_naked_pair_x(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_pair_board))
        vals = {4, 7}
        x = 0
        should_contain_before = [True, True, False, True, True, True, False, True, False]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain(should_contain_before, col_possibilities, vals)
        sp.naked_pair_x(x)
        should_contain_after = [True, False, False, False, True, False, False, False, False]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain(should_contain_after, col_possibilities, vals)

    def test_naked_pair_block(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_pair_block_board))
        vals = {8, 9}
        block_num = 4
        should_contain_before = [True, True, False, True, True, True, True, True, True]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain(should_contain_before, block_possibilities, vals)
        sp.naked_pair_block(block_num)
        should_contain_after = [False, True, False, False, False, True, False, False, False]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain(should_contain_after, block_possibilities, vals)

    # endregion
    ###############################################################################################################
    # Naked tuple tests
    # http://hodoku.sourceforge.net/en/tech_naked.php
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    ###############################################################################################################
    # region

    def test_naked_tuple_y_2(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.naked_pair_board)))
        vals = {4, 7}
        y = 0
        should_contain_before = [True, True, False, True, True, True, False, True, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain_before, row_possibilities, vals)
        sp.naked_tuple_y(y, 2)
        should_contain_after = [True, False, False, False, True, False, False, False, False]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain(should_contain_after, row_possibilities, vals)

    def test_naked_tuple_x_2(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_pair_board))
        vals = {4, 7}
        x = 0
        should_contain_before = [True, True, False, True, True, True, False, True, False]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain(should_contain_before, col_possibilities, vals)
        sp.naked_tuple_x(x, 2)
        should_contain_after = [True, False, False, False, True, False, False, False, False]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain(should_contain_after, col_possibilities, vals)

    def test_naked_tuple_block_2(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_pair_block_board))
        vals = {8, 9}
        block_num = 4
        should_contain_before = [True, True, False, True, True, True, True, True, True]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain(should_contain_before, block_possibilities, vals)
        sp.naked_tuple_block(block_num, 2)
        should_contain_after = [False, True, False, False, False, True, False, False, False]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain(should_contain_after, block_possibilities, vals)

    def test_naked_tuple_y_3(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.naked_triple_board)))
        vals = {3, 6, 9}
        y = 1
        should_contain_before = [1, 2, 0, 2, 3, 0, 0, 0, 0]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_before, row_possibilities, vals)
        sp.naked_tuple_y(y, 3)
        should_contain_after = [0, 2, 0, 2, 3, 0, 0, 0, 0]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_after, row_possibilities, vals)

    def test_naked_tuple_x_3(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_triple_board))
        vals = {3, 6, 9}
        x = 1
        should_contain_before = [1, 2, 0, 2, 3, 0, 0, 0, 0]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_before, col_possibilities, vals)
        sp.naked_tuple_x(x, 3)
        should_contain_after = [0, 2, 0, 2, 3, 0, 0, 0, 0]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_after, col_possibilities, vals)

    def test_naked_tuple_block_3(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_triple_block_board))
        vals = {1, 2, 6}
        block_num = 1
        should_contain_any_before = [3, 3, 3, 2, 2, 2, 3, 3, 3]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_any_before, block_possibilities, vals)
        sp.naked_tuple_block(block_num, 3)
        should_contain_any_after = [0, 3, 0, 0, 0, 0, 3, 3, 0]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_any_after, block_possibilities, vals)

    def test_naked_tuple_y_4(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_quad_board))
        vals = {3, 4, 8, 9}
        y = 7
        should_contain_before = [4, 0, 3, 2, 0, 2, 2, 1, 0]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_before, row_possibilities, vals)
        sp.naked_tuple_y(y, 4)
        should_contain_after = [4, 0, 3, 2, 0, 2, 0, 0, 0]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_after, row_possibilities, vals)

    def test_naked_tuple_x_4(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.naked_quad_board)))
        vals = {3, 4, 8, 9}
        x = 7
        should_contain_before = [4, 0, 3, 2, 0, 2, 2, 1, 0]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_before, col_possibilities, vals)
        sp.naked_tuple_x(x, 4)
        should_contain_after = [4, 0, 3, 2, 0, 2, 0, 0, 0]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_after, col_possibilities, vals)

    def test_naked_tuple_block_4(self):
        sp = SudokuPuzzle(self.get_board_copy(self.naked_quad_block_board))
        vals = {4, 6, 7, 9}
        block_num = 6
        should_contain_before = [2, 3, 4, 1, 2, 3, 2, 2, 3]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_before, block_possibilities, vals)
        sp.naked_tuple_block(block_num, 4)
        should_contain_after = [0, 0, 4, 0, 2, 3, 0, 0, 3]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_after, block_possibilities, vals)

    # endregion
    ###############################################################################################################
    # Hidden subset tests
    # http://hodoku.sourceforge.net/en/tech_hidden.php
    ###############################################################################################################
    # region

    def test_hidden_subset_row_2(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.hidden_pair_board)))
        vals = {1, 9}
        y = 8
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [3, 2, 1, 2, 1, 1, 0, 1, 3]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_before, row_possibilities, excluded_vals)
        sp.hidden_subset_row(y, 2)
        should_contain_after = [3, 2, 1, 2, 0, 1, 0, 1, 3]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_after, row_possibilities, excluded_vals)

    def test_hidden_subset_col_2(self):
        sp = SudokuPuzzle(self.get_board_copy(self.hidden_pair_board))
        vals = {1, 9}
        x = 8
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [3, 2, 1, 2, 1, 1, 0, 1, 3]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_before, col_possibilities, excluded_vals)
        sp.hidden_subset_col(x, 2)
        should_contain_after = [3, 2, 1, 2, 0, 1, 0, 1, 3]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_after, col_possibilities, excluded_vals)

    def test_hidden_subset_block_2(self):
        sp = SudokuPuzzle(self.get_board_copy(self.hidden_pair_block_board))
        vals = {4, 7}
        block_num = 0
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [5, 5, 5, 3, 3, 3, 4, 4, 1]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_before, block_possibilities, excluded_vals)
        sp.hidden_subset_block(block_num, 2)
        should_contain_after = [0, 0, 5, 3, 3, 3, 4, 4, 1]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_after, block_possibilities, excluded_vals)

    def test_hidden_subset_row_3(self):
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.hidden_triple_board)))
        vals = {2, 5, 6}
        y = 5
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [2, 3, 4, 4, 5, 3, 1, 4, 3]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_before, row_possibilities, excluded_vals)
        sp.hidden_subset_row(y, 3)
        should_contain_after = [2, 3, 4, 0, 5, 0, 1, 0, 3]
        row_possibilities = sp.enumerate_row_possibilities(y)
        self.assert_should_contain_count(should_contain_after, row_possibilities, excluded_vals)

    def test_hidden_subset_col_3(self):
        sp = SudokuPuzzle(self.get_board_copy(self.hidden_triple_board))
        vals = {2, 5, 6}
        x = 5
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [2, 3, 4, 4, 5, 3, 1, 4, 3]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_before, col_possibilities, excluded_vals)
        sp.hidden_subset_col(x, 3)
        should_contain_after = [2, 3, 4, 0, 5, 0, 1, 0, 3]
        col_possibilities = sp.enumerate_col_possibilities(x)
        self.assert_should_contain_count(should_contain_after, col_possibilities, excluded_vals)

    def test_hidden_subset_block_3(self):
        sp = SudokuPuzzle(self.get_board_copy(self.hidden_triple_block_board))
        vals = {2, 4, 5}
        block_num = 6
        excluded_vals = all_possibilities.difference(vals)
        should_contain_before = [3, 1, 2, 2, 0, 1, 2, 1, 1]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_before, block_possibilities, excluded_vals)
        sp.hidden_subset_block(block_num, 3)
        should_contain_after = [3, 1, 2, 2, 0, 1, 2, 0, 0]
        block_possibilities = sp.enumerate_block_possibilities(block_num)
        self.assert_should_contain_count(should_contain_after, block_possibilities, excluded_vals)

    # endregion
    ###############################################################################################################
    # X-Wing/Basic fish tests
    # http://hodoku.sourceforge.net/en/tech_fishb.php
    ###############################################################################################################
    # region

    def test_basic_fish_in_rows(self):
        y1 = 1
        y2 = 4
        x1 = 4
        x2 = 7
        val = 5
        sp = SudokuPuzzle(self.get_board_copy(self.basic_fish_row_board))
        should_contain_before_x1 = [False, True, False, True, True, False, False, False, False]
        should_contain_before_x2 = [False, True, False, False, True, False, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        self.assert_should_contain(should_contain_before_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_before_x2, x2_possibilities, {val})
        sp.basic_fish_in_rows(y1, y2)
        should_contain_after_x1 = [False, True, False, False, True, False, False, False, False]
        should_contain_after_x2 = [False, True, False, False, True, False, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        self.assert_should_contain(should_contain_after_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_after_x2, x2_possibilities, {val})

    def test_basic_fish_in_cols(self):
        x1 = 0
        x2 = 4
        y1 = 1
        y2 = 4
        val = 1
        sp = SudokuPuzzle(self.get_board_copy(self.basic_fish_col_board))
        should_contain_before_y1 = [True, False, False, True, True, False, True, True, True]
        should_contain_before_y2 = [True, False, True, True, True, False, True, True, True]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        self.assert_should_contain(should_contain_before_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_before_y2, y2_possibilities, {val})
        sp.basic_fish_in_cols(x1, x2)
        should_contain_after_y1 = [True, False, False, False, True, False, False, False, False]
        should_contain_after_y2 = [True, False, False, False, True, False, False, False, False]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        self.assert_should_contain(should_contain_after_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_after_y2, y2_possibilities, {val})

    def test_fish_3_in_rows(self):
        y1 = 1
        y2 = 2
        y3 = 8
        x1 = 0
        x2 = 4
        x3 = 7
        val = 2
        sp = SudokuPuzzle(self.get_board_copy(self.fish_3_row_board))
        should_contain_before_x1 = [False, True, False, False, False, False, True, False, True]
        should_contain_before_x2 = [False, True, True, False, False, False, False, False, False]
        should_contain_before_x3 = [False, False, True, False, False, True, False, False, True]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        self.assert_should_contain(should_contain_before_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_before_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_before_x3, x3_possibilities, {val})
        sp.fish_in_rows({y1, y2, y3})
        should_contain_after_x1 = [False, True, False, False, False, False, False, False, True]
        should_contain_after_x2 = [False, True, True, False, False, False, False, False, False]
        should_contain_after_x3 = [False, False, True, False, False, False, False, False, True]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        self.assert_should_contain(should_contain_after_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_after_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_after_x3, x3_possibilities, {val})

    def test_fish_3_in_rows_2(self):
        y1 = 1
        y2 = 3
        y3 = 6
        x1 = 1
        x2 = 2
        x3 = 4
        val = 4
        sp = SudokuPuzzle(self.get_board_copy(self.fish_3_row_board_2))
        should_contain_before_x1 = [False, True, True, True, False, True, False, True, True]
        should_contain_before_x2 = [False, True, True, True, False, True, True, True, True]
        should_contain_before_x3 = [False, True, True, True, False, True, True, True, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        self.assert_should_contain(should_contain_before_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_before_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_before_x3, x3_possibilities, {val})
        sp.fish_in_rows({y1, y2, y3})
        should_contain_after_x1 = [False, True, False, True, False, False, False, False, False]
        should_contain_after_x2 = [False, True, False, True, False, False, True, False, False]
        should_contain_after_x3 = [False, True, False, True, False, False, True, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        self.assert_should_contain(should_contain_after_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_after_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_after_x3, x3_possibilities, {val})

    def test_fish_3_in_cols(self):
        x1 = 1
        x2 = 2
        x3 = 8
        y1 = 0
        y2 = 4
        y3 = 7
        val = 2
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.fish_3_row_board)))
        should_contain_before_y1 = [False, True, False, False, False, False, True, False, True]
        should_contain_before_y2 = [False, True, True, False, False, False, False, False, False]
        should_contain_before_y3 = [False, False, True, False, False, True, False, False, True]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        y3_possibilities = sp.enumerate_row_possibilities(y3)
        self.assert_should_contain(should_contain_before_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_before_y2, y2_possibilities, {val})
        self.assert_should_contain(should_contain_before_y3, y3_possibilities, {val})
        sp.fish_in_cols({x1, x2, x3})
        should_contain_after_y1 = [False, True, False, False, False, False, False, False, True]
        should_contain_after_y2 = [False, True, True, False, False, False, False, False, False]
        should_contain_after_y3 = [False, False, True, False, False, False, False, False, True]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        y3_possibilities = sp.enumerate_row_possibilities(y3)
        self.assert_should_contain(should_contain_after_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_after_y2, y2_possibilities, {val})
        self.assert_should_contain(should_contain_after_y3, y3_possibilities, {val})

    def test_fish_3_in_cols_2(self):
        x1 = 1
        x2 = 3
        x3 = 6
        y1 = 1
        y2 = 2
        y3 = 4
        val = 4
        sp = SudokuPuzzle(self.get_board_copy(SudokuPuzzle.reflect_board_over_xy(self.fish_3_row_board_2)))
        should_contain_before_y1 = [False, True, True, True, False, True, False, True, True]
        should_contain_before_y2 = [False, True, True, True, False, True, True, True, True]
        should_contain_before_y3 = [False, True, True, True, False, True, True, True, False]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        y3_possibilities = sp.enumerate_row_possibilities(y3)
        self.assert_should_contain(should_contain_before_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_before_y2, y2_possibilities, {val})
        self.assert_should_contain(should_contain_before_y3, y3_possibilities, {val})
        sp.fish_in_cols({x1, x2, x3})
        should_contain_after_y1 = [False, True, False, True, False, False, False, False, False]
        should_contain_after_y2 = [False, True, False, True, False, False, True, False, False]
        should_contain_after_y3 = [False, True, False, True, False, False, True, False, False]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        y3_possibilities = sp.enumerate_row_possibilities(y3)
        self.assert_should_contain(should_contain_after_y1, y1_possibilities, {val})
        self.assert_should_contain(should_contain_after_y2, y2_possibilities, {val})
        self.assert_should_contain(should_contain_after_y3, y3_possibilities, {val})

    def test_fish_4_in_rows(self):
        y1 = 2
        y2 = 3
        y3 = 5
        y4 = 6
        x1 = 0
        x2 = 1
        x3 = 4
        x4 = 8
        val = 7
        sp = SudokuPuzzle(self.get_board_copy(self.fish_4_row_board))
        should_contain_before_x1 = [False, True, True, True, True, True, True, False, False]
        should_contain_before_x2 = [True, False, True, True, True, True, True, False, True]
        should_contain_before_x3 = [True, False, True, True, False, True, True, False, True]
        should_contain_before_x4 = [False, True, True, True, True, True, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        x4_possibilities = sp.enumerate_col_possibilities(x4)
        self.assert_should_contain(should_contain_before_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_before_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_before_x3, x3_possibilities, {val})
        self.assert_should_contain(should_contain_before_x4, x4_possibilities, {val})
        sp.fish_in_rows({y1, y2, y3, y4})
        should_contain_after_x1 = [False, False, True, True, False, True, True, False, False]
        should_contain_after_x2 = [False, False, True, True, False, True, True, False, False]
        should_contain_after_x3 = [False, False, True, True, False, True, True, False, False]
        should_contain_after_x4 = [False, False, True, True, False, True, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        x3_possibilities = sp.enumerate_col_possibilities(x3)
        x4_possibilities = sp.enumerate_col_possibilities(x4)
        self.assert_should_contain(should_contain_after_x1, x1_possibilities, {val})
        self.assert_should_contain(should_contain_after_x2, x2_possibilities, {val})
        self.assert_should_contain(should_contain_after_x3, x3_possibilities, {val})
        self.assert_should_contain(should_contain_after_x4, x4_possibilities, {val})

    # endregion
    ###############################################################################################################
    # Single Digit Patterns
    # http://hodoku.sourceforge.net/en/tech_sdp.php
    ###############################################################################################################
    # region

    def test_skyscraper_rows(self):
        sp = SudokuPuzzle(self.get_board_copy(self.skyscraper_row_board))
        candidate = 1
        y1 = 0
        y2 = 2
        should_contain_before_y1 = [False, False, False, True, True, True, True, True, False]
        should_contain_before_y2 = [False, False, False, True, True, False, False, False, True]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        self.assert_should_contain(should_contain_before_y1, y1_possibilities, {candidate})
        self.assert_should_contain(should_contain_before_y2, y2_possibilities, {candidate})
        sp.skyscraper_in_rows(candidate)
        should_contain_after_y1 = [False, False, False, True, True, True, False, False, False]
        should_contain_after_y2 = [False, False, False, False, False, False, False, False, True]
        y1_possibilities = sp.enumerate_row_possibilities(y1)
        y2_possibilities = sp.enumerate_row_possibilities(y2)
        self.assert_should_contain(should_contain_after_y1, y1_possibilities, {candidate})
        self.assert_should_contain(should_contain_after_y2, y2_possibilities, {candidate})

    def test_skyscraper_cols(self):
        sp = SudokuPuzzle(self.get_board_copy(self.skyscraper_col_board))
        candidate = 4
        x1 = 3
        x2 = 4
        should_contain_before_x1 = [True, False, False, False, False, False, True, True, False]
        should_contain_before_x2 = [False, True, False, False, True, False, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        self.assert_should_contain(should_contain_before_x1, x1_possibilities, {candidate})
        self.assert_should_contain(should_contain_before_x2, x2_possibilities, {candidate})
        sp.skyscraper_in_cols(candidate)
        should_contain_after_x1 = [False, False, False, False, False, False, True, True, False]
        should_contain_after_x2 = [False, True, False, False, True, False, False, False, False]
        x1_possibilities = sp.enumerate_col_possibilities(x1)
        x2_possibilities = sp.enumerate_col_possibilities(x2)
        self.assert_should_contain(should_contain_after_x1, x1_possibilities, {candidate})
        self.assert_should_contain(should_contain_after_x2, x2_possibilities, {candidate})

    def test_kite(self):
        sp = SudokuPuzzle(self.get_board_copy(self.kite_board))
        candidate = 5
        p = sp.get_possibilities()
        self.assertSetEqual(p[1][3], {5, 7})
        sp.kite(candidate)
        p = sp.get_possibilities()
        self.assertSetEqual(p[1][3], {7})

    def test_dual_kite(self):
        sp = SudokuPuzzle(self.get_board_copy(self.dual_kite_board))
        candidate = 1
        p = sp.get_possibilities()
        self.assertSetEqual(p[3][8], {1, 9})
        self.assertSetEqual(p[5][7], {1, 6})
        sp.kite(candidate)
        sp.kite(candidate)
        p = sp.get_possibilities()
        # Assert the candidiates were removed from both ends of the string
        self.assertSetEqual(p[3][8], {9})
        self.assertSetEqual(p[5][7], {6})
        # Assert the kite strings stayed the same
        self.assertSetEqual(p[0][2], {1, 8})
        self.assertSetEqual(p[0][7], {1, 8})
        self.assertSetEqual(p[2][0], {1, 7})
        self.assertSetEqual(p[2][8], {1, 7})
        self.assertSetEqual(p[3][2], {1, 8, 9})
        self.assertSetEqual(p[5][0], {1, 4, 9})
    # endregion
    ###############################################################################################################
    # Guessing
    ###############################################################################################################
    # region

    def test_make_guess(self):
        sp = SudokuPuzzle(self.get_board_copy(self.guess_board))
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, None, None, None, None, None, None])
        self.assert_missing_row_possibilities(sp, 8, [{1}, {2}, {3}, None, None, None, None, None, None])
        # Guess 1.0
        sp.make_guess(sp.board[0][3], 4)
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, None, None, None, None, None])
        self.assert_missing_row_possibilities(sp, 8, [{1}, {2}, {3}, {4}, None, None, None, None, None])
        # Guess 2.0
        sp.make_guess(sp.board[0][4], 5)
        sp.set_val_in_puzzle(0, 8, 9)
        sp.remove_possibility_from_puzzle_by_loc(8, 0, 2)
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, 5, None, None, None, 9])
        self.assert_missing_row_possibilities(sp, 8, [{1, 2}, {2}, {3}, {4}, {5}, None, None, None, {9}])
        # Guess 3.0
        sp.make_guess(sp.board[0][5], 6)
        sp.set_val_in_puzzle(0, 7, 8)
        sp.remove_possibility_from_puzzle_by_loc(8, 1, 3)
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, 5, 6, None, 8, 9])
        self.assert_missing_row_possibilities(sp, 8, [{1, 2}, {2, 3}, {3}, {4}, {5}, {6}, None, {8}, {9}])
        p = sp.get_possibilities()
        # Guesses 1.0, 2.0, 3.0 still apply
        self.assertTrue(p[0][5] == {6})
        self.assertTrue(p[0][4] == {5})
        self.assertTrue(p[0][3] == {4})
        self.assertTrue(sp.cells_dict[sp.board[0][5]].val == 6)
        self.assertTrue(sp.cells_dict[sp.board[0][4]].val == 5)
        self.assertTrue(sp.cells_dict[sp.board[0][3]].val == 4)
        # Revert Guess 3.0
        sp.revert_guess()
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, 5, None, None, None, 9])
        self.assert_missing_row_possibilities(sp, 8, [{1, 2}, {2}, {3}, {4}, {5}, None, None, None, {9}])
        p = sp.get_possibilities()
        # The guess from 3.0 should still apply (the candidate should be removed.
        # However, the val should no longer be set. Guesses 1.0, 2.0 still apply.
        self.assertTrue(6 not in p[0][5])
        self.assertTrue(p[0][4] == {5})
        self.assertTrue(p[0][3] == {4})
        self.assertTrue(sp.cells_dict[sp.board[0][5]].val is None)
        self.assertTrue(sp.cells_dict[sp.board[0][4]].val == 5)
        self.assertTrue(sp.cells_dict[sp.board[0][3]].val == 4)
        # Guess 3.1
        sp.make_guess(sp.board[0][5], 7)
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, 5, 7, None, None, 9])
        self.assert_missing_row_possibilities(sp, 8, [{1, 2}, {2}, {3}, {4}, {5}, {7}, None, None, {9}])
        p = sp.get_possibilities()
        # We made another guess (3.1) after rolling back 3.0 so the removed possibilities from 3.0 still apply
        # So should guesses 1.0, 2.0, 3.1
        self.assertTrue(p[0][5] == {7})
        self.assertTrue(6 not in p[0][5])
        self.assertTrue(p[0][4] == {5})
        self.assertTrue(p[0][3] == {4})
        self.assertTrue(sp.cells_dict[sp.board[0][5]].val == 7)
        self.assertTrue(sp.cells_dict[sp.board[0][4]].val == 5)
        self.assertTrue(sp.cells_dict[sp.board[0][3]].val == 4)
        # Revert Guess 3.1
        sp.revert_guess()
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, 5, None, None, None, 9])
        self.assert_missing_row_possibilities(sp, 8, [{1, 2}, {2}, {3}, {4}, {5}, None, None, None, {9}])
        p = sp.get_possibilities()
        # We have now back in 2.0 after rolling back 3.0, 3.1 so their eliminated guesses still apply
        # So should guesses 1.0, 2.0
        self.assertTrue(6 not in p[0][5])
        self.assertTrue(7 not in p[0][5])
        self.assertTrue(p[0][4] == {5})
        self.assertTrue(p[0][3] == {4})
        self.assertTrue(sp.cells_dict[sp.board[0][4]].val == 5)
        self.assertTrue(sp.cells_dict[sp.board[0][3]].val == 4)
        # Revert Guess 2.0
        sp.revert_guess()
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, 4, None, None, None, None, None])
        self.assert_missing_row_possibilities(sp, 8, [{1}, {2}, {3}, {4}, None, None, None, None, None])
        p = sp.get_possibilities()
        # The removed guesses from 3.1, 3.2 no longer apply since we rolled back twice
        # THe possibility from 2.0 should still be removed. However, the val should no longer be set.
        # Now only guess 1.0 applies.
        self.assertTrue(6 in p[0][5])
        self.assertTrue(7 in p[0][5])
        self.assertTrue(5 not in p[0][4])
        self.assertTrue(p[0][3] == {4})
        self.assertTrue(sp.cells_dict[sp.board[0][3]].val == 4)
        # Revert Guess 1
        sp.revert_guess()
        self.assert_row_contains_candidates(sp, 0, [1, 2, 3, None, None, None, None, None, None])
        self.assert_missing_row_possibilities(sp, 8, [{1}, {2}, {3}, None, None, None, None, None, None])
        p = sp.get_possibilities()
        # The removed guesses from 2.0, 3.0, 3.1 no longer apply since we rolled back at least 2 times
        # Now only guess 1.0 applies
        self.assertTrue(6 in p[0][5])
        self.assertTrue(7 in p[0][5])
        self.assertTrue(5 in p[0][4])
        self.assertTrue(4 not in p[0][3])

    def test_validate_updated_cells_missing_candidate(self):
        sp = SudokuPuzzle(self.get_board_copy(self.missing_candidate_validation_board))
        cell_name = sp.board[2][8]
        # Can't remove the candidate or else we can't place it in the row
        sp.remove_possibility_from_puzzle_by_cell_name(cell_name, 1)
        try:
            sp.validate_updated_cells([(cell_name, 1)])
            self.assertFalse("Expected a BadGuessError")
        except BadGuessError as bge:
            self.assertEqual(bge.cell_name, cell_name)
            self.assertEqual(bge.val, 1)
            self.assertEqual(bge.message, "Can't place 1 in row 2")

    def test_validate_updated_cells_empty_possibilities(self):
        sp = SudokuPuzzle(self.get_board_copy(self.empty_possibilities_validation_board))
        cell_name = sp.board[5][8]
        # Can't remove the candidates from the cell or else possibilities would be empty
        sp.remove_possibility_from_puzzle_by_cell_name(cell_name, 8)
        sp.remove_possibility_from_puzzle_by_cell_name(cell_name, 9)
        try:
            sp.validate_updated_cells([(cell_name, 8), (cell_name, 9)])
            self.assertFalse("Expected a BadGuessError")
        except BadGuessError as bge:
            self.assertEqual(bge.cell_name, cell_name)
            self.assertEqual(bge.val, 8)
            self.assertEqual(bge.message, "No more possibilities for cell c585")

    # endregion

    ###############################################################################################################
    # Board Validation
    ###############################################################################################################
    # region Board Validation

    def test_validate_board(self):
        try:
            sp = SudokuPuzzle(self.get_board_copy(self.illegal_puzzle_board))
        except BadPuzzleError as bpe:
            self.assertSetEqual(bpe.illegal_cells, {'c000', 'c082', 'c120', 'c523'})

    # endregion
    ###############################################################################################################
    # Helper methods
    ###############################################################################################################

    # region Board Rotation/Reflection
    def test_rotate_board_cw(self):
        expected_rotated_board = [
            [None, None, None, None, 2, None, None, None, None],
            [None, None, None, None, 9, None, None, None, None],
            [None, None, None, None, None, None, None, 8, None],
            [None, 8, None, None, None, None, None, None, None],
            [None, None, None, None, 1, None, None, None, None],
            [None, None, None, None, 4, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None]
        ]
        self.assertListEqual(SudokuPuzzle.rotate_board_cw(self.block_block_board), expected_rotated_board)
        self.assertListEqual(SudokuPuzzle.rotate_board_cw(self.block_block_board, 4), self.block_block_board)

    def test_rotate_board_ccw(self):
        expected_rotated_board = [
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, 4, None, None, None, None],
            [None, None, None, None, 1, None, None, None, None],
            [None, None, None, None, None, None, None, 8, None],
            [None, 8, None, None, None, None, None, None, None],
            [None, None, None, None, 9, None, None, None, None],
            [None, None, None, None, 2, None, None, None, None]
        ]
        self.assertListEqual(SudokuPuzzle.rotate_board_ccw(self.block_block_board), expected_rotated_board)
        self.assertListEqual(SudokuPuzzle.rotate_board_ccw(self.block_block_board, 4), self.block_block_board)

    def test_rotate_board(self):
        sb_cw = SudokuPuzzle(SudokuPuzzle.rotate_board_cw(self.block_block_board))
        sb_ccw = SudokuPuzzle(SudokuPuzzle.rotate_board_ccw(self.block_block_board))

        sb_cw2 = SudokuPuzzle(SudokuPuzzle.rotate_board_cw(self.block_block_board, 2))
        sb_ccw2 = SudokuPuzzle(SudokuPuzzle.rotate_board_ccw(self.block_block_board, 2))

        sb_cw3 = SudokuPuzzle(SudokuPuzzle.rotate_board_cw(self.block_block_board, 3))
        sb_ccw3 = SudokuPuzzle(SudokuPuzzle.rotate_board_ccw(self.block_block_board, 3))

        self.assert_sps_equal(sb_cw, sb_ccw3)
        self.assert_sps_equal(sb_cw2, sb_ccw2)
        self.assert_sps_equal(sb_cw3, sb_ccw)

        # Rotating cw then ccw should stay the same
        self.assertListEqual(SudokuPuzzle.rotate_board_ccw(
            SudokuPuzzle.rotate_board_cw(self.block_block_board)), self.block_block_board)

    def test_reflect_board_over_xy(self):
        expected_reflected_board = [
            [1, None, None, None, None, None, None, None, 4],
            [2, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, 7, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, 6, None, None, None, None, None],
            [3, None, None, None, None, None, None, None, 8]
        ]
        sp = SudokuPuzzle(SudokuPuzzle.reflect_board_over_xy(self.get_board_copy(self.rotation_board)))
        self.assert_sp_board_equal(sp, expected_reflected_board)
        sp2 = SudokuPuzzle(SudokuPuzzle.reflect_board_over_xy(SudokuPuzzle.reflect_board_over_xy(self.get_board_copy(
            self.rotation_board))))
        self.assert_sp_board_equal(sp2, self.rotation_board)
    # endregion

    # region Assert Should Contain

    def assert_should_contain(self, should_contain, possibilities, vals):
        """
        :param should_contain: Length n list containing True/False
        :param possibilities: Length n list containing sets of possibilities
        :param vals: The values to check that are in possibilities
        Asserts that vals is a subset of possibilities[k] iff should_contain[k] == true
        """
        if len(possibilities) != len(should_contain):
            self.fail("should_contain and possibilities do not have the same length")
        for k in range(0, len(possibilities)):
            contains = vals.issubset(possibilities[k])
            self.assertTrue(contains == should_contain[k])

    def assert_should_contain_count(self, should_contain_count, possibilities, vals):
        """
        :param should_contain_count: Length n list containing ints
        :param possibilities: Length n list containing sets of possibilities
        :param vals: The values to check that are in possibilities
        Asserts that intersection between vals and possibilities[k] has length == should_contain_n[k]
        """
        if len(possibilities) != len(should_contain_count):
            self.fail("should_contain_n and possibilities do not have the same length")
        for k in range(0, len(possibilities)):
            count = len(possibilities[k].intersection(vals))
            # print(k, possibilities[k].intersection(vals), count, should_contain_count[k])
            self.assertTrue(count == should_contain_count[k])

    # endregion

    # region Assert Board Equality
    def assert_sp_board_equal(self, sp, expected_board):
        for y in all_locs:
            for x in all_locs:
                self.assertEqual(sp.cells_dict[sp.board[y][x]].val, expected_board[y][x])

    def assert_sps_equal(self, sp1, sp2):
        for y in all_locs:
            for x in all_locs:
                self.assertEqual(sp1.cells_dict[sp1.board[y][x]].val, sp2.cells_dict[sp2.board[y][x]].val)
    # endregion

    def assert_loc_contains_candidate(self, sp, y, x, candidate):
        self.assertEqual(sp.cells_dict[sp.board[y][x]].val, candidate)

    def assert_row_contains_candidates(self, sp, y, candidates):
        for x in all_locs:
            self.assertEqual(sp.cells_dict[sp.board[y][x]].val, candidates[x])

    def assert_missing_row_possibilities(self, sp, y, removed_possibilities):
        for x in all_locs:
            if removed_possibilities[x] is not None:
                self.assertSetEqual(sp.cells_dict[sp.board[y][x]].possibilities,
                                    all_possibilities.difference(removed_possibilities[x]))
            else:
                self.assertSetEqual(sp.cells_dict[sp.board[y][x]].possibilities, all_possibilities)

if __name__ == '__main__':
    pass
    # suite = unittest.TestSuite()
    # suite.addTest(TestSudokuPuzzle("test_naked_pair_y"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
