import copy
import unittest
from SudokuPuzzle import SudokuPuzzle
from SudokuHelper import all_locs
from SudokuHelper import all_possibilities

__author__ = 'william'


class TestSudokuPuzzle(unittest.TestCase):

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

        expected_locs_left_by_y_0 = {1: set(), 2: set(), 3: set(), 4: set(), 5: {1, 3},
                                     6: set(), 7: set(), 8: {1, 8}, 9: {3, 8}}
        expected_locs_left_by_y_1 = {1: {2}, 2: {3, 6, 7, 8}, 3: {2, 7}, 4: {7, 8}, 5: {0, 3, 6},
                                     6: set(), 7: set(), 8: set(), 9: {0, 3, 6, 7, 8}}
        self.assertDictEqual(sp.locs_left_by_y[0], expected_locs_left_by_y_0)
        self.assertDictEqual(sp.locs_left_by_y[1], expected_locs_left_by_y_1)

        expected_locs_left_by_x_0 = {1: set(), 2: {6, 8}, 3: set(), 4: set(), 5: {1, 2, 6},
                                     6: {6, 7}, 7: {2, 6, 7}, 8: set(), 9: {1, 2}}
        expected_locs_left_by_x_1 = {1: {6, 7}, 2: {4, 5, 6}, 3: {2, 6, 7}, 4: set(), 5: {0, 2, 6},
                                     6: set(), 7: {2, 4, 5, 6, 7}, 8: {0, 2}, 9: set()}
        self.assertDictEqual(sp.locs_left_by_x[0], expected_locs_left_by_x_0)
        self.assertDictEqual(sp.locs_left_by_x[1], expected_locs_left_by_x_1)

        expected_locs_left_by_block_0 = {1: {5}, 2: set(), 3: {5, 7, 8}, 4: set(), 5: {1, 3, 6, 7},
                                         6: set(), 7: {6, 7, 8}, 8: {1, 7}, 9: {3, 6}}
        expected_locs_left_by_block_7 = {1: {0}, 2: set(), 3: {2, 5}, 4: set(), 5: set(),
                                         6: {0, 2, 5}, 7: set(), 8: {5, 8}, 9: set()}

        self.assertDictEqual(sp.locs_left_by_block[0], expected_locs_left_by_block_0)
        self.assertDictEqual(sp.locs_left_by_block[7], expected_locs_left_by_block_7)

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

    def test_fill_unique_candidates(self):
        sp = SudokuPuzzle(self.get_board_copy(self.unique_candidate_board))
        (cell_y, cell_x) = (0, 7)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidates_y(0)
        self.assertEqual(cell.val, 4)

        sp = SudokuPuzzle(SudokuPuzzle.reflect_board_over_xy(self.get_board_copy(self.unique_candidate_board)))
        (cell_y, cell_x) = (7, 0)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidates_x(0)
        self.assertEqual(cell.val, 4)

        sp = SudokuPuzzle(self.get_board_copy(self.unique_candidate_block_board))
        (cell_y, cell_x) = (0, 5)
        cell = sp.cells_dict[sp.board[cell_y][cell_x]]
        self.assertEqual(cell.val, None)
        sp.fill_unique_candidates()
        self.assertEqual(cell.val, 4)

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

    def test_get_naked_pairs_in_possibilities_dict(self):
        possibility_dict = {0: [4, 7], 1: [2, 3], 3: [2, 3], 6: [4, 7], 8: [0, 7], 9: [2, 3]}
        naked_pairs = SudokuPuzzle.get_naked_pairs_in_possibilities_dict(possibility_dict)
        self.assertListEqual(naked_pairs, [(0, 6), (1, 3), (1, 9), (3, 9)])

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

    def assert_sp_board_equal(self, sp, expected_board):
        for y in all_locs:
            for x in all_locs:
                self.assertEqual(sp.cells_dict[sp.board[y][x]].val, expected_board[y][x])

    def assert_sps_equal(self, sp1, sp2):
        for y in all_locs:
            for x in all_locs:
                self.assertEqual(sp1.cells_dict[sp1.board[y][x]].val, sp2.cells_dict[sp2.board[y][x]].val)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSudokuPuzzle("test_naked_pair_y"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main()