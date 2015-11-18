import copy
import unittest
from SudokuPuzzle import SudokuPuzzle
from SudokuHelper import all_locs
from SudokuHelper import all_possibilities

__author__ = 'william'


class TestSudokuBoard(unittest.TestCase):

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

    def get_board_copy(self, board):
        return copy.deepcopy(board)

    def test_init_possibilities(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        board = sp.get_board()
        self.assertListEqual(board, self.get_board_copy(self.test_board))

        expected_possibilities = [
            [set(), {8, 5}, set(), {9, 5}, set(), set(), set(), set(), {8, 9}],
            [{9, 5}, set(), {1, 3}, {9, 2, 5}, set(), set(), {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}],
            [{9, 5, 7}, {8, 3, 5, 7}, {3, 7}, {9, 2, 5, 6}, set(), {9, 5, 6}, set(), {9, 2, 3}, {8, 9, 2}],
            [set(), set(), {4, 7}, {1, 5}, {1, 7}, set(), set(), {7}, set()],
            [set(), {2, 7}, set(), {8, 9, 6}, {6, 7}, {8, 9, 6}, set(), {9, 2, 7}, set()],
            [set(), {2, 7}, set(), set(), {7}, {9, 4}, {9, 2}, set(), set()],
            [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, set(), {1, 6}, set(), {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}],
            [{6, 7}, {1, 3, 7}, {1, 3, 7}, set(), set(), {8, 3, 6}, {8, 9}, set(), {8, 9, 7}],
            [{2}, set(), set(), set(), set(), {8}, set(), {1, 2}, set()]
        ]
        p = sp.get_possibilities()
        self.assertListEqual(p, expected_possibilities)

    def test_init_remaining_in(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        expected_remaining_in_y = [
            {5, 8, 9}, {1, 2, 3, 4, 5, 9}, {2, 3, 5, 7, 8, 9},
            {1, 5, 7}, {2, 6, 7, 9}, {4},
            {1, 2, 3, 4, 5, 6, 7}, {1, 6, 7, 8, 9}, {1, 2, 8}
        ]
        self.assertListEqual(sp.remaining_in_y, expected_remaining_in_y)

        expected_remaining_in_x = [
            {5, 6, 7, 9}, {1, 2, 3, 5, 7, 8}, {1, 3, 4, 7},
            {1, 2, 5, 6, 8, 9}, {1, 6, 7}, {4, 8, 9},
            {2, 5, 8, 9}, {1, 2, 3, 4, 7, 9}, {2, 4, 8, 9}
        ]
        self.assertListEqual(sp.remaining_in_x, expected_remaining_in_x)

        expected_remaining_in_blocks = [
            {1, 3, 5, 7, 8, 9}, {2, 5, 9}, {2, 3, 4, 5, 8, 9},
            {4, 7}, {1, 6, 7, 9}, {2, 9},
            {1, 2, 3, 5, 6, 7}, {1, 6, 8}, {1, 2, 4, 7, 8, 9}
        ]
        self.assertListEqual(sp.remaining_in_blocks, expected_remaining_in_blocks)

    def test_init_locs_left_by(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        expected_possibilities = [
            [set(), {8, 5}, set(), {9, 5}, set(), set(), set(), set(), {8, 9}],
            [{9, 5}, set(), {1, 3}, {9, 2, 5}, set(), set(), {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}],
            [{9, 5, 7}, {8, 3, 5, 7}, {3, 7}, {9, 2, 5, 6}, set(), {9, 5, 6}, set(), {9, 2, 3}, {8, 9, 2}],
            [set(), set(), {4, 7}, {1, 5}, {1, 7}, set(), set(), {7}, set()],
            [set(), {2, 7}, set(), {8, 9, 6}, {6, 7}, {8, 9, 6}, set(), {9, 2, 7}, set()],
            [set(), {2, 7}, set(), set(), {7}, {9, 4}, {9, 2}, set(), set()],
            [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, set(), {1, 6}, set(), {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}],
            [{6, 7}, {1, 3, 7}, {1, 3, 7}, set(), set(), {8, 3, 6}, {8, 9}, set(), {8, 9, 7}],
            [{2}, set(), set(), set(), set(), {8}, set(), {1, 2}, set()]
        ]
        p = sp.get_possibilities()

        self.assertListEqual(p, expected_possibilities)

        expected_locs_left_by_y = [
            
        ]


    def test_enumerate_possibilities_by_row(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        row_1_possibilities = sp.enumerate_row_possibilities(1)
        self.assertListEqual(row_1_possibilities, [{9, 5}, set(), {1, 3}, {9, 2, 5}, set(), set(), {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}])
        row_6_possibilities = sp.enumerate_row_possibilities(6)
        self.assertListEqual(row_6_possibilities, [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, set(), {1, 6}, set(), {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}])

    def test_enumerate_possibilities_by_col(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        col_1_possibilities = sp.enumerate_col_possibilities(1)
        self.assertListEqual(col_1_possibilities, [{8, 5}, set(), {8, 3, 5, 7}, set(), {2, 7},
                                                   {2, 7}, {1, 2, 3, 5, 7}, {1, 3, 7}, set()])
        col_6_possibilities = sp.enumerate_col_possibilities(6)
        self.assertListEqual(col_6_possibilities, [set(), {9, 2, 5}, set(), set(), set(),
                                                   {9, 2}, {2}, {8, 9}, set()])

    def test_enumerate_possibilities_by_block(self):
        sp = SudokuPuzzle(self.get_board_copy(self.test_board))
        block_1_possibilities = sp.enumerate_block_possibilities(1)
        self.assertListEqual(block_1_possibilities, [{9, 5}, set(), set(), {9, 2, 5}, set(), set(), {9, 2, 5, 6}, set(), {9, 5, 6}])
        block_6_possibilities = sp.enumerate_block_possibilities(6)
        self.assertListEqual(block_6_possibilities, [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, set(), {6, 7},
                                                     {1, 3, 7}, {1, 3, 7}, {2}, set(), set()])

    def test_fill_sole_candidates(self):
        sp = SudokuPuzzle(self.get_board_copy(self.sole_candidate_board))
        (cell_y, cell_x) = (5, 5)
        p = sp.get_possibilities()
        for y in all_locs:
            self.assertTrue(5 in p[y][5] or len(p[y][cell_x]) == 0)
        for x in all_locs:
            self.assertTrue(5 in p[5][x] or len(p[cell_y][x]) == 0)
        sp.fill_sole_candidates()
        new_p = sp.get_possibilities()
        for y in all_locs:
            self.assertTrue(5 not in new_p[y][cell_x])
        for x in all_locs:
            self.assertTrue(5 not in new_p[cell_y][x])

    def assert_board_equal(self, sp, expected_board):
        for y in all_locs:
            for x in all_locs:
                self.assertEqual(sp.cells_dict[sp.board[y][x]].val, expected_board[y][x])