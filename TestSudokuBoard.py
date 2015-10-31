import unittest
from SudokuBoard import SudokuBoard

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

    def test_calculate_possibilities_init(self):
        sb = SudokuBoard(self.test_board)
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





        sb.print_board()
        print(sb.possibilities)

        # self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()

