import unittest
import copy
from SudokuBoard import SudokuBoard

__author__ = 'william'


class TestSudokuBoard(unittest.TestCase):

    empty_board = [[None for _ in range(0, 9)] for _ in range(0, 9)]
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

    naked_subset = [
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

    naked_subset_in_block = [
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

    def get_test_board(self):
        return copy.deepcopy(self.test_board)

    def get_empty_board(self):
        return copy.deepcopy(self.empty_board)

    def get_block_block_board(self):
        return copy.deepcopy(self.block_block_board)

    def test_calculate_possibilities_init(self):
        sb = SudokuBoard(self.get_test_board())
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
        expected_rows = [{1, 2, 3, 4, 6, 7}, {8, 6, 7}, {1, 4}, {8, 9, 2, 3, 6}, {1, 3, 4, 5}, {8, 1, 3, 5, 6}, {8, 9}, {2, 4, 5}, {3, 4, 5, 6, 7, 9}]
        expected_cols = [{8, 1, 3, 4}, {9, 4, 6}, {8, 9, 2, 5, 6}, {3, 4, 7}, {2, 3, 4, 5, 8, 9}, {1, 2, 7}, {1, 3, 4, 6, 7}, {8, 5, 6}, {1, 3, 5, 6}]
        expected_blocks = [{2, 4, 6}, {8, 1, 3, 4, 7}, {1, 6, 7}, {1, 3, 5, 6, 8, 9}, {2, 3}, {1, 3, 4, 5, 6, 8}, {8, 9, 4}, {9, 2, 4, 5, 7}, {3, 5, 6}]

        self.assertListEqual(sb.possibilities, expected_possibilities)
        self.assertListEqual(sb.rows, expected_rows)
        self.assertListEqual(sb.cols, expected_cols)
        self.assertListEqual(sb.blocks, expected_blocks)

    def test_fill_sole_candidates(self):
        sb = SudokuBoard(self.get_test_board())
        possibilities = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
        possibilities[2][3] = {9}
        possibilities[3][4] = {1, 2}
        possibilities[4][5] = {4}

        sb.possibilities = possibilities
        sb.fill_sole_candidates()

        self.assertEqual(sb.board[2][3], 9)
        self.assertEqual(sb.board[4][5], 4)

    def test_loc_to_block_num(self):
        self.assertEquals(SudokuBoard.loc_to_block_num(2, 1), 0)
        self.assertEquals(SudokuBoard.loc_to_block_num(3, 1), 3)
        self.assertEquals(SudokuBoard.loc_to_block_num(8, 6), 8)

    def test_cell_num_to_block_offsets(self):
        self.assertEquals(SudokuBoard.cell_num_to_block_offsets(1), (0, 1))
        self.assertEquals(SudokuBoard.cell_num_to_block_offsets(5), (1, 2))
        self.assertEquals(SudokuBoard.cell_num_to_block_offsets(8), (2, 2))

    def test_block_num_to_board_offsets(self):
        self.assertEquals(SudokuBoard.block_num_to_board_offsets(1), (0, 3))
        self.assertEquals(SudokuBoard.block_num_to_board_offsets(5), (3, 6))
        self.assertEquals(SudokuBoard.block_num_to_board_offsets(8), (6, 6))

    def test_row_possibilities_to_numbered_cells(self):
        sb = SudokuBoard(self.get_test_board())
        cell_nums = [i for i in range(0, 9)]
        possibilities_row_1 = [{9, 5}, set(), {1, 3}, {9, 2, 5}, set(), set(), {9, 2, 5}, {9, 2, 3, 4}, {9, 2, 4}]
        self.assertDictEqual(sb.row_possibilities_to_numbered_cells(1), dict(zip(cell_nums, possibilities_row_1)))
        possibilities_row_6 = [{2, 5, 6, 7}, {1, 2, 3, 5, 7}, set(), {1, 6}, set(), {3, 6}, {2}, {1, 2, 4, 7}, {2, 4, 7}]
        self.assertDictEqual(sb.row_possibilities_to_numbered_cells(6), dict(zip(cell_nums, possibilities_row_6)))

    def test_col_possibilities_to_numbered_cells(self):
        sb = SudokuBoard(self.get_test_board())
        cell_nums = [i for i in range(0, 9)]
        possibilities_col_1 = [{8, 5}, set(), {8, 3, 5, 7}, set(), {2, 7}, {2, 7}, {1, 2, 3, 5, 7}, {1, 3, 7}, set()]
        self.assertDictEqual(sb.col_possibilities_to_numbered_cells(1), dict(zip(cell_nums, possibilities_col_1)))
        possibilities_col_6 = [set(), {9, 2, 5}, set(), set(), set(), {9, 2}, {2}, {8, 9}, set()]
        self.assertDictEqual(sb.col_possibilities_to_numbered_cells(6), dict(zip(cell_nums, possibilities_col_6)))

    def test_block_possibilities_to_numbered_cells(self):
        sb = SudokuBoard(self.get_test_board())
        cell_nums = [i for i in range(0, 9)]
        possibilities_block_3 = [set(), set(), {4, 7}, set(), {2, 7}, set(), set(), {2, 7}, set()]
        self.assertDictEqual(sb.block_possibilities_to_numbered_cells(3), dict(zip(cell_nums, possibilities_block_3)))

    def test_find_val_with_count_in_numbered_cells(self):
        values = {1, 2, 3}
        numbered_sets = dict(zip([i for i in range(0, 5)], [{1, 3}, {4}, set(), {1, 2}, set()]))
        d1 = SudokuBoard.find_val_with_count_in_numbered_cells(values, numbered_sets, 1)
        d2 = SudokuBoard.find_val_with_count_in_numbered_cells(values, numbered_sets, 2)
        d1_expected = {
            3: [0],
            2: [3]
        }
        d2_expected = {
            1: [0, 3]
        }
        self.assertDictEqual(d1, d1_expected)
        self.assertDictEqual(d2, d2_expected)

    # def test_print(self):
    #     sb = SudokuBoard(self.get_test_board())
    #     sb.print_possibilities()

    def test_set_board_with_row_dict(self):
        sb = SudokuBoard(self.get_empty_board())
        sb.set_board_with_row_dict(2, {1: [1, 7], 7: [2], 8: [3]})
        self.assertEqual(sb.board[2][1], 1)
        self.assertEqual(sb.board[2][7], 1)
        self.assertEqual(sb.board[2][2], 7)
        self.assertEqual(sb.board[2][3], 8)

    def test_set_board_with_col_dict(self):
        sb = SudokuBoard(self.get_empty_board())
        sb.set_board_with_col_dict(2, {1: [1, 7], 7: [2], 8: [3]})
        self.assertEqual(sb.board[1][2], 1)
        self.assertEqual(sb.board[7][2], 1)
        self.assertEqual(sb.board[2][2], 7)
        self.assertEqual(sb.board[3][2], 8)

    def test_set_board_with_block_dict(self):
        sb = SudokuBoard(self.get_empty_board())
        sb.set_board_with_block_dict(2, {1: [1, 7], 7: [2], 8: [3]})
        self.assertEqual(sb.board[0][7], 1)
        self.assertEqual(sb.board[2][7], 1)
        self.assertEqual(sb.board[0][8], 7)
        self.assertEqual(sb.board[1][6], 8)

    def test_fill_unique_candidates(self):
        sb = SudokuBoard(self.get_empty_board())

        sb.board[0][2] = 4
        sb.board[4][1] = 4
        sb.board[8][5] = 4
        sb.board[6][0] = 5
        sb.calculate_possibilities()
        sb.fill_unique_candidates()
        self.assertEqual(sb.board[7][0], 4)

    def test_block_rc_interaction(self):
        sb = SudokuBoard(self.get_empty_board())

        sb.board[0][4] = 7
        sb.board[3][3] = 2
        sb.board[3][5] = 1
        sb.board[5][3] = 9
        sb.board[5][5] = 6
        sb.calculate_possibilities()
        for i in [0, 1, 2, 3, 5, 6, 7, 8]:
            self.assertTrue(7 in sb.possibilities[4][i])
        for i in [4]:
            self.assertTrue(7 not in sb.possibilities[4][i])
        sb.block_rc_interaction(4)
        for i in [3, 5]:
            self.assertTrue(7 in sb.possibilities[4][i])
        for i in [0, 1, 2, 4, 6, 7, 8]:
            self.assertTrue(7 not in sb.possibilities[4][i])

    def test_eliminate_row_possibilities(self):
        block_num = 3
        y_block, _ = SudokuBoard.block_num_to_board_offsets(block_num)
        y_block_offset = 1
        y = y_block + y_block_offset
        val = 4

        sb = SudokuBoard(self.get_empty_board())

        for x in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            self.assertTrue(val in sb.possibilities[y][x])

        sb.eliminate_row_possibilities_by_block_dict(block_num, {val: [y_block_offset]})
        for x in [3, 4, 5, 6, 7, 8]:
            self.assertTrue(val not in sb.possibilities[y][x])
        for x in [0, 1, 2]:
            self.assertTrue(val in sb.possibilities[y][x])

    def test_eliminate_col_possibilities(self):
        block_num = 6
        _, x_block = SudokuBoard.block_num_to_board_offsets(block_num)
        x_block_offset = 2
        x = x_block + x_block_offset
        val = 4

        sb = SudokuBoard(self.get_empty_board())

        for y in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            self.assertTrue(val in sb.possibilities[y][x])

        sb.eliminate_col_possibilities_by_block_dict(block_num, {val: [x_block_offset]})
        for y in [0, 1, 2, 3, 4, 5]:
            self.assertTrue(val not in sb.possibilities[y][x])
        for y in [6, 7, 8]:
            self.assertTrue(val in sb.possibilities[y][x])

    def test_block_block_by_row_interaction(self):
        sb = SudokuBoard(self.get_block_block_board())
        val = 8

        sb.calculate_possibilities()
        for i in [0, 1, 4, 5, 6, 7, 8]:
            self.assertTrue(val in sb.possibilities[3][i])
            self.assertTrue(val in sb.possibilities[5][i])
        for i in [2, 3]:
            self.assertTrue(val not in sb.possibilities[3][i])
            self.assertTrue(val not in sb.possibilities[5][i])

        sb.block_block_by_block_row_interaction(1, 2)
        for i in [0, 1, 4, 5]:
            self.assertTrue(val in sb.possibilities[3][i])
            self.assertTrue(val in sb.possibilities[5][i])
        for i in [2, 3, 6, 7, 8]:
            self.assertTrue(val not in sb.possibilities[3][i])
            self.assertTrue(val not in sb.possibilities[5][i])

    def test_block_block_by_col_interaction(self):
        sb = SudokuBoard(self.get_empty_board())
        val = 8
        sb.board[5][7] = val
        sb.board[6][1] = val
        sb.board[3][4] = 4
        sb.board[4][4] = 1
        sb.board[7][4] = 9
        sb.board[8][4] = 2
        sb.calculate_possibilities()
        for i in [0, 1, 2, 3, 4, 7, 8]:
            self.assertTrue(val in sb.possibilities[i][3])
            self.assertTrue(val in sb.possibilities[i][5])
        for i in [5, 6]:
            self.assertTrue(val not in sb.possibilities[i][3])
            self.assertTrue(val not in sb.possibilities[i][5])

        sb.block_block_by_block_col_interaction(1, 0)
        for i in [3, 4, 7, 8]:
            self.assertTrue(val in sb.possibilities[i][3])
            self.assertTrue(val in sb.possibilities[i][5])
        for i in [0, 1, 2, 5, 6]:
            self.assertTrue(val not in sb.possibilities[i][3])
            self.assertTrue(val not in sb.possibilities[i][5])

    def test_all_board_board_interactions(self):
        sb = SudokuBoard(self.get_block_block_board())
        val = 8

        sb.calculate_possibilities()
        for i in [0, 1, 4, 5, 6, 7, 8]:
            self.assertTrue(val in sb.possibilities[3][i])
            self.assertTrue(val in sb.possibilities[5][i])
        for i in [2, 3]:
            self.assertTrue(val not in sb.possibilities[3][i])
            self.assertTrue(val not in sb.possibilities[5][i])

        sb.all_block_block_interactions()
        for i in [0, 1, 4, 5]:
            self.assertTrue(val in sb.possibilities[3][i])
            self.assertTrue(val in sb.possibilities[5][i])
        for i in [2, 3, 6, 7, 8]:
            self.assertTrue(val not in sb.possibilities[3][i])
            self.assertTrue(val not in sb.possibilities[5][i])

    def test_naked_pair_in_row(self):
        sb = SudokuBoard(SudokuBoard.rotate_board_cw(self.naked_subset))
        for i in [1, 3, 4, 5, 7, 8]:
            self.assertTrue(4 in sb.possibilities[0][i] and 7 in sb.possibilities[0][i])
        for i in [0, 2, 6]:
            self.assertTrue(7 not in sb.possibilities[0][i] and 4 not in sb.possibilities[0][i])
        sb.naked_pair_in_row(0)
        sb.print_possibilities()
        for i in [4, 8]:
            self.assertTrue(4 in sb.possibilities[0][i] and 7 in sb.possibilities[0][i])
        for i in [0, 1, 2, 3, 5, 6, 7]:
            self.assertTrue(4 not in sb.possibilities[0][i] and 7 not in sb.possibilities[0][i])

    def test_naked_pair_in_col(self):
        sb = SudokuBoard(self.naked_subset)
        for i in [0, 1, 3, 4, 5, 7]:
            self.assertTrue(4 in sb.possibilities[i][0] and 7 in sb.possibilities[i][0])
        for i in [2, 6, 8]:
            self.assertTrue(7 not in sb.possibilities[i][0] and 4 not in sb.possibilities[i][0])
        sb.naked_pair_in_col(0)
        for i in [0, 4]:
            self.assertTrue(4 in sb.possibilities[i][0] and 7 in sb.possibilities[i][0])
        for i in [1, 2, 3, 5, 6, 7, 8]:
            self.assertTrue(4 not in sb.possibilities[i][0] and 7 not in sb.possibilities[i][0])

    def test_naked_pair_in_block(self):
        sb = SudokuBoard(self.naked_subset_in_block)
        sb.print_possibilities()
        self.assertTrue(sb.possibilities[3][3] == {5, 8, 9})
        self.assertTrue(sb.possibilities[3][4] == {8, 9})
        self.assertTrue(sb.possibilities[3][5] == set())
        self.assertTrue(sb.possibilities[4][3] == {1, 2, 4, 8, 9})
        self.assertTrue(sb.possibilities[4][4] == {1, 2, 4, 8, 9})
        self.assertTrue(sb.possibilities[4][5] == {8, 9})
        self.assertTrue(sb.possibilities[5][3] == {4, 5, 6, 8, 9})
        self.assertTrue(sb.possibilities[5][4] == {3, 4, 6, 8, 9})
        self.assertTrue(sb.possibilities[5][5] == {3, 5, 8, 9})
        sb.naked_pair_in_block(4)
        self.assertTrue(sb.possibilities[3][3] == {5})
        self.assertTrue(sb.possibilities[3][4] == {8, 9})
        self.assertTrue(sb.possibilities[3][5] == set())
        self.assertTrue(sb.possibilities[4][3] == {1, 2, 4})
        self.assertTrue(sb.possibilities[4][4] == {1, 2, 4})
        self.assertTrue(sb.possibilities[4][5] == {8, 9})
        self.assertTrue(sb.possibilities[5][3] == {4, 5, 6})
        self.assertTrue(sb.possibilities[5][4] == {3, 4, 6})
        self.assertTrue(sb.possibilities[5][5] == {3, 5})



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
        self.assertListEqual(SudokuBoard.rotate_board_cw(self.block_block_board), expected_rotated_board)
        self.assertListEqual(SudokuBoard.rotate_board_cw(self.block_block_board, 4), self.block_block_board)

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
        self.assertListEqual(SudokuBoard.rotate_board_ccw(self.block_block_board), expected_rotated_board)
        self.assertListEqual(SudokuBoard.rotate_board_ccw(self.block_block_board, 4), self.block_block_board)

    def test_rotate_board(self):
        sb_cw = SudokuBoard(SudokuBoard.rotate_board_cw(self.block_block_board))
        sb_ccw = SudokuBoard(SudokuBoard.rotate_board_ccw(self.block_block_board))

        sb_cw2 = SudokuBoard(SudokuBoard.rotate_board_cw(self.block_block_board, 2))
        sb_ccw2 = SudokuBoard(SudokuBoard.rotate_board_ccw(self.block_block_board, 2))

        sb_cw3 = SudokuBoard(SudokuBoard.rotate_board_cw(self.block_block_board, 3))
        sb_ccw3 = SudokuBoard(SudokuBoard.rotate_board_ccw(self.block_block_board, 3))

        self.assertListEqual(sb_cw.board, sb_ccw3.board)
        self.assertListEqual(sb_cw2.board, sb_ccw2.board)
        self.assertListEqual(sb_cw3.board, sb_ccw.board)

        # Rotating cw then ccw should stay the same
        self.assertListEqual(
            SudokuBoard.rotate_board_ccw(SudokuBoard.rotate_board_cw(self.block_block_board)),
            self.block_block_board
        )

if __name__ == '__main__':
    unittest.main()

